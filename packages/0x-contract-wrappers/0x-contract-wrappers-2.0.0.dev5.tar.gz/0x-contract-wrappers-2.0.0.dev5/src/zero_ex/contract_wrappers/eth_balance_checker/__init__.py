"""Generated wrapper for EthBalanceChecker Solidity contract."""

# pylint: disable=too-many-arguments

import json
from typing import (  # pylint: disable=unused-import
    Any,
    List,
    Optional,
    Tuple,
    Union,
)

from eth_utils import to_checksum_address
from mypy_extensions import TypedDict  # pylint: disable=unused-import
from hexbytes import HexBytes
from web3 import Web3
from web3.contract import ContractFunction
from web3.datastructures import AttributeDict
from web3.providers.base import BaseProvider

from zero_ex.contract_wrappers.bases import ContractMethod, Validator
from zero_ex.contract_wrappers.tx_params import TxParams


# Try to import a custom validator class definition; if there isn't one,
# declare one that we can instantiate for the default argument to the
# constructor for EthBalanceChecker below.
try:
    # both mypy and pylint complain about what we're doing here, but this
    # works just fine, so their messages have been disabled here.
    from . import (  # type: ignore # pylint: disable=import-self
        EthBalanceCheckerValidator,
    )
except ImportError:

    class EthBalanceCheckerValidator(  # type: ignore
        Validator
    ):
        """No-op input validator."""


try:
    from .middleware import MIDDLEWARE  # type: ignore
except ImportError:
    pass


class GetEthBalancesMethod(ContractMethod):
    """Various interfaces to the getEthBalances method."""

    def __init__(
        self,
        web3_or_provider: Union[Web3, BaseProvider],
        contract_address: str,
        contract_function: ContractFunction,
        validator: Validator = None,
    ):
        """Persist instance data."""
        super().__init__(web3_or_provider, contract_address, validator)
        self.underlying_method = contract_function

    def validate_and_normalize_inputs(self, addresses: List[str]):
        """Validate the inputs to the getEthBalances method."""
        self.validator.assert_valid(
            method_name="getEthBalances",
            parameter_name="addresses",
            argument_value=addresses,
        )
        return addresses

    def call(
        self, addresses: List[str], tx_params: Optional[TxParams] = None
    ) -> List[int]:
        """Execute underlying contract method via eth_call.

        Batch fetches ETH balances

        :param addresses: Array of addresses.
        :param tx_params: transaction parameters
        :returns: Array of ETH balances.
        """
        (addresses) = self.validate_and_normalize_inputs(addresses)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(addresses).call(tx_params.as_dict())

    def send_transaction(
        self, addresses: List[str], tx_params: Optional[TxParams] = None
    ) -> Union[HexBytes, bytes]:
        """Execute underlying contract method via eth_sendTransaction.

        Batch fetches ETH balances

        :param addresses: Array of addresses.
        :param tx_params: transaction parameters
        :returns: Array of ETH balances.
        """
        (addresses) = self.validate_and_normalize_inputs(addresses)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(addresses).transact(tx_params.as_dict())

    def estimate_gas(
        self, addresses: List[str], tx_params: Optional[TxParams] = None
    ) -> int:
        """Estimate gas consumption of method call."""
        (addresses) = self.validate_and_normalize_inputs(addresses)
        tx_params = super().normalize_tx_params(tx_params)
        return self.underlying_method(addresses).estimateGas(
            tx_params.as_dict()
        )


# pylint: disable=too-many-public-methods,too-many-instance-attributes
class EthBalanceChecker:
    """Wrapper class for EthBalanceChecker Solidity contract."""

    get_eth_balances: GetEthBalancesMethod
    """Constructor-initialized instance of
    :class:`GetEthBalancesMethod`.
    """

    def __init__(
        self,
        web3_or_provider: Union[Web3, BaseProvider],
        contract_address: str,
        validator: EthBalanceCheckerValidator = None,
    ):
        """Get an instance of wrapper for smart contract.

        :param web3_or_provider: Either an instance of `web3.Web3`:code: or
            `web3.providers.base.BaseProvider`:code:
        :param contract_address: where the contract has been deployed
        :param validator: for validation of method inputs.
        """
        # pylint: disable=too-many-statements

        self.contract_address = contract_address

        if not validator:
            validator = EthBalanceCheckerValidator(
                web3_or_provider, contract_address
            )

        web3 = None
        if isinstance(web3_or_provider, BaseProvider):
            web3 = Web3(web3_or_provider)
        elif isinstance(web3_or_provider, Web3):
            web3 = web3_or_provider
        if web3 is None:
            raise TypeError(
                "Expected parameter 'web3_or_provider' to be an instance of either"
                + " Web3 or BaseProvider"
            )

        # if any middleware was imported, inject it
        try:
            MIDDLEWARE
        except NameError:
            pass
        else:
            try:
                for middleware in MIDDLEWARE:
                    web3.middleware_onion.inject(
                        middleware["function"], layer=middleware["layer"]
                    )
            except ValueError as value_error:
                if value_error.args == (
                    "You can't add the same un-named instance twice",
                ):
                    pass

        self._web3_eth = web3.eth

        functions = self._web3_eth.contract(
            address=to_checksum_address(contract_address),
            abi=EthBalanceChecker.abi(),
        ).functions

        self.get_eth_balances = GetEthBalancesMethod(
            web3_or_provider,
            contract_address,
            functions.getEthBalances,
            validator,
        )

    @staticmethod
    def abi():
        """Return the ABI to the underlying contract."""
        return json.loads(
            '[{"constant":true,"inputs":[{"internalType":"address[]","name":"addresses","type":"address[]"}],"name":"getEthBalances","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"}]'  # noqa: E501 (line-too-long)
        )


# pylint: disable=too-many-lines
