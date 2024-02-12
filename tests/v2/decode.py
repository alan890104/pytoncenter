import pytest
from pytoncenter.v2.api import AsyncTonCenterClientV2
from pytoncenter.address import Address
from pytoncenter.decoder import JettonDataDecoder, Types, Decoder

pytest_plugins = ("pytest_asyncio",)


class TestDecoder:
    client: AsyncTonCenterClientV2

    def setup_method(self):
        self.client = AsyncTonCenterClientV2(network="testnet")

    @pytest.mark.asyncio
    async def test_get_jetton_data(self):
        result = await self.client.run_get_method("kQBqSpvo4S87mX9tjHaG4zhYZeORhVhMapBJpnMZ64jhrP-A", "get_jetton_data", {})
        decoder = JettonDataDecoder()
        output = decoder.decode(result)
        assert output["mintable"] == True
        assert output["admin_address"] == Address("0:bccc51ccf0b08ca7d5ecfbec3783dc267fb470b83809710b55fa81d94520aa41")

    @pytest.mark.asyncio
    async def test_get_custom_data(self):
        result = await self.client.run_get_method("kQCpk40ub48fvx89vSUjOTRy0vOEEZ4crOPPfLEvg88q1EeH", "getOracleData", {})
        OracleMetaDataDecoder = Decoder(
            Types.Address("base_asset_address"),
            Types.Address("quote_asset_address"),
            Types.Number("base_asset_decimals"),
            Types.Number("quote_asset_decimals"),
            Types.Number("min_base_asset_threshold"),
            Types.Address("base_asset_wallet_address"),
            Types.Address("quote_asset_wallet_address"),
            Types.Bool("is_initialized"),
            Types.Number("latestBaseAssetPrice"),
            Types.Number("latestTimestamp"),
        )
        output = OracleMetaDataDecoder.decode(result)
        assert output["base_asset_address"] == Address("0:0000000000000000000000000000000000000000000000000000000000000000")
        assert output["base_asset_decimals"] == 9
        assert output["is_initialized"] == True
        assert output["min_base_asset_threshold"] == 1000000000
