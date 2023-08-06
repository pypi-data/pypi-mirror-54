"""Static shape analysis for numpy"""

from typing import List

from mypy.nodes import NameExpr, UnaryExpr
from mypy.plugin import Plugin
from mypy.types import TupleType, Instance


def get_node_dims(node_type: Instance) -> list:
    """Get a nodes shape.

    A node type is shaped if there is a Tuple type in its
    arguments which denotes dimensions.

    """
    items: List = []
    if hasattr(node_type, "args"):
        if node_type.args:
            if isinstance(node_type.args[0], TupleType):
                items = node_type.args[0].items

    return items


def handle_np_elementwise(method_sig_ctx) -> Instance:
    """Handle the shapes of elementwise ops.

    Addtly, deal with broadcasting if necessary.

    """

    def get_named_expr_dims(operand) -> list:
        dims: List = []
        if isinstance(operand, NameExpr):
            dims = get_node_dims(operand.node.type)
        return dims

    left_dims = get_named_expr_dims(method_sig_ctx.context.left)
    right_dims = get_named_expr_dims(method_sig_ctx.context.right)

    return_type = method_sig_ctx.default_return_type

    if left_dims and right_dims:
        for i in range(max(len(left_dims) - 1, len(right_dims) - 1), -1, -1):
            if i < len(left_dims) and i < len(right_dims):
                if left_dims[i] != right_dims[i]:
                    method_sig_ctx.api.fail(
                        f"Broadcasting Problem: the {i}'th dimension does not match for arguments with shapes {left_dims} and {right_dims}.",
                        method_sig_ctx.context,
                    )

        if len(left_dims) == len(right_dims):
            return_type = method_sig_ctx.context.left.node.type
        elif len(left_dims) > len(right_dims):
            return_type = method_sig_ctx.context.left.node.type
        else:
            return_type = method_sig_ctx.context.right.node.type

    elif left_dims:
        return_type = method_sig_ctx.context.left.node.type

    elif right_dims:
        return_type = method_sig_ctx.context.right.node.type

    type_args = [] if not return_type.args else [return_type.args[0].copy_modified()]

    return Instance(
        return_type.type,
        type_args,
        line=method_sig_ctx.default_return_type.line,
        column=method_sig_ctx.default_return_type.column,
    )


def handle_matmul(method_sig_ctx, arg_x, arg_y) -> Instance:
    """Infer matrix multiplication return types."""
    arg_x_dims = get_node_dims(arg_x.type)
    arg_y_dims = get_node_dims(arg_y.type)

    return_type = method_sig_ctx.default_return_type
    type_args = []

    if arg_x_dims and arg_y_dims:
        if (len(arg_x_dims) == 1 and len(arg_y_dims) == 1) or (
            len(arg_x_dims) == 1 and len(arg_y_dims) >= 1
        ):
            if arg_x_dims[0] != arg_y_dims[0]:
                message = f"Dimension mismatch: {arg_x_dims[0]} != {arg_y_dims[0]}"
                method_sig_ctx.api.fail(message, method_sig_ctx.context)
            return_type = arg_x.type
        elif len(arg_x_dims) >= 1 and len(arg_y_dims) == 1:
            if arg_x_dims[-1] != arg_y_dims[0]:
                message = f"Dimension mismatch: {arg_x_dims[-1]} != {arg_y_dims[0]}"
                method_sig_ctx.api.fail(message, method_sig_ctx.context)
        elif len(arg_x_dims) >= 1 and len(arg_y_dims) >= 1:
            if arg_x_dims[-1] != arg_y_dims[-2]:
                message = f"Dimension mismatch: {arg_x_dims[-1]} != {arg_y_dims[-2]}"
                method_sig_ctx.api.fail(message, method_sig_ctx.context)
            elif not all(x == y for x, y in zip(arg_x_dims[:-2], arg_y_dims[:-2])):
                message = (
                    f"Dimension mismatch (Broadcasting): {arg_x_dims} != {arg_y_dims}"
                )
                method_sig_ctx.api.fail(message, method_sig_ctx.context)
            else:
                return_type = arg_x.type
                type_args = [
                    arg_x.type.args[0].copy_modified(
                        items=arg_x.type.args[0].items[:-2]
                        + [arg_x.type.args[0].items[-2], arg_y.type.args[0].items[-1]]
                    )
                ]

    return Instance(
        return_type.type,
        type_args,
        line=method_sig_ctx.default_return_type.line,
        column=method_sig_ctx.default_return_type.column,
    )


def handle_transpose(method_sig_ctx) -> Instance:
    """Compute shape type for transpose.

    Reverse dimensions.
    """
    dims = get_node_dims(method_sig_ctx.type)
    if dims:
        dims = list(reversed(dims))
    return method_sig_ctx.type.copy_modified(
        args=[method_sig_ctx.type.args[0].copy_modified(items=dims)]
    )


def handle_np_matmul(method_sig_ctx) -> Instance:
    """Compute return type for np.matmul calls."""
    arg_x = method_sig_ctx.args[0][0].node
    arg_y = method_sig_ctx.args[1][0].node
    return handle_matmul(method_sig_ctx, arg_x, arg_y)


def handle_np_at_matmul(method_sig_ctx) -> Instance:
    """Compute return type for @ matmul function."""
    arg_x = method_sig_ctx
    arg_y = method_sig_ctx.args[0][0].node
    return handle_matmul(method_sig_ctx, arg_x, arg_y)


def handle_np_reduction(method_sig_ctx) -> Instance:
    """Compute dimensions for the result of a reduction.

    First, we find the integer corresponding to the dim.
    Finally, we remove that shape in the list of dims
    and return the type.
    """

    def get_reduction_dim():
        """Get reduction dimension."""
        if method_sig_ctx.context.args:
            # A negative signed dimension was provided
            if (
                isinstance(method_sig_ctx.context.args[0], UnaryExpr)
                and method_sig_ctx.context.args[0].op == "-"
            ):
                arg_val = dict(
                    zip(
                        method_sig_ctx.context.arg_names,
                        [
                            None
                            if not hasattr(x, "expr") and not hasattr(x.expr, "value")
                            else x.expr.value
                            for x in method_sig_ctx.context.args
                        ],
                    )
                )
                if arg_val.get("axis") is not None:
                    reduction_dim = -arg_val["axis"]
                elif arg_val.get(None) is not None:
                    reduction_dim = -arg_val[None]
            else:
                # Parse arg values and get the axis dim
                arg_val = dict(
                    zip(
                        method_sig_ctx.context.arg_names,
                        [
                            None if not hasattr(x, "value") else x.value
                            for x in method_sig_ctx.context.args
                        ],
                    )
                )
                if arg_val.get("axis") is not None:
                    reduction_dim = arg_val["axis"]
                elif arg_val.get(None) is not None:
                    reduction_dim = arg_val[None]
        return reduction_dim

    reduction_dim = get_reduction_dim()

    return_type = method_sig_ctx.default_return_type
    type_args = []

    if reduction_dim is not None:
        if reduction_dim == -1:
            type_args = [
                method_sig_ctx.type.args[0].copy_modified(
                    items=method_sig_ctx.type.args[0].items[:reduction_dim]
                )
            ]
        else:
            if hasattr(method_sig_ctx, "type"):
                return_type = method_sig_ctx.type
            else:
                return_type = method_sig_ctx.args[0][0].node.type

            type_args = [
                return_type.args[0].copy_modified(
                    items=(
                        return_type.args[0].items[:reduction_dim]
                        + return_type.args[0].items[reduction_dim + 1 :]
                    )
                )
            ]

    return Instance(
        return_type.type,
        type_args,
        line=method_sig_ctx.default_return_type.line,
        column=method_sig_ctx.default_return_type.column,
    )


class ShapeTypePlugin(Plugin):
    """Mypy plugin for shape-types."""

    def get_attribute_hook(self, fullname: str):
        """Compute attribute return types."""
        if fullname == "numpy._ArrayOrScalarCommon.T":
            return handle_transpose

    def get_function_hook(self, fullname: str):
        """Compute function return types."""
        reduction_ops = set(["numpy.sum", "numpy.mean", "numpy.average", "numpy.prod"])
        if fullname == "numpy.matmul":
            return handle_np_matmul
        if fullname in reduction_ops:
            return handle_np_reduction

    def get_method_hook(self, fullname: str):
        """Compute method return types."""
        # see explanation below
        element_wise_ops = set(
            [
                "numpy.ndarray.__mul__",
                "numpy.ndarray.__sub__",
                "numpy.ndarray.__add__",
                "numpy.ndarray.__div__",
            ]
        )
        reduction_ops = set(
            ["numpy.ndarray.sum", "numpy.ndarray.mean", "numpy.ndarray.prod"]
        )
        if fullname in element_wise_ops:
            return handle_np_elementwise
        elif fullname in reduction_ops:
            return handle_np_reduction
        elif fullname == "numpy.ndarray.__matmul__":
            return handle_np_at_matmul


def plugin(version: str):
    return ShapeTypePlugin
