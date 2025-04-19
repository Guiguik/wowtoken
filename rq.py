from blizzardapi2 import BlizzardApi

client_id = '07a204009d624d859473ae46d12bb2e8'
client_secret = 'AYytStp1C2PUKuCTc9r4WCbQZ29JDTO4'

api_client = BlizzardApi(client_id, client_secret)

# Unprotected API endpoint
categories_index = api_client.wow.game_data.get_achievement_categories_index("us", "en_US")

# Protected API endpoint
summary = api_client.wow.profile.get_account_profile_summary("us", "en_US", "access_token")

# Wow Classic endpoint
connected_realms_index = api_client.wow.game_data.get_connected_realms_index("us", "en_US", is_classic=True)

