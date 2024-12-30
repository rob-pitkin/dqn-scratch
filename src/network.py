import torch
import torch.nn as nn


class QNetwork(nn.Module):
    """
    Feedforward MLP for the QNetwork (and target network)

    Attributes:
        input_dim (int): input size of the network, typically the size of the observation space
        output_dim (int): output size of the network, typically the size of the action space
        activation_fn (str): activation function, one of "relu" or "tanh"
        hidden_num (int): number of hidden layers
        hidden_dims (List): list of hidden layer sizes from layer 0 to n
    """

    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        activation_fn: str,
        hidden_num: int = None,
        hidden_dims: list[int] = None,
    ):
        super(QNetwork, self).__init__()
        if (
            input_dim < 1
            or (hidden_dims and any([h < 1 for h in hidden_dims]))
            or output_dim < 1
        ):
            raise ValueError("All dimension values must be >= 1")
        if activation_fn != "relu" and activation_fn != "tanh":
            raise ValueError("Supported activation functions: 'relu', 'tanh'")
        layer_sizes = (
            [input_dim] + hidden_dims + [output_dim]
            if hidden_dims
            else [input_dim, output_dim]
        )

        self.layers = []
        for i in range(len(layer_sizes) - 1):
            self.layers.append(nn.Linear(layer_sizes[i], layer_sizes[i + 1]))

        self.activation = None
        if activation_fn == "relu":
            self.activation = nn.ReLU()
        else:
            self.activation = nn.Tanh()

    def forward(self, x: torch.tensor) -> torch.tensor:
        """
        Forward pass of the Q value network

        Args:
            x (torch.tensor): the input tensor to the network

        Returns:
            torch.tensor: a tensor with the values for each output
        """
        for i in range(len(self.layers) - 1):
            x = self.layers[i](x)
            x = self.activation(x)
        return self.layers[-1](x)