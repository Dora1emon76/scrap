from telethon.sync import TelegramClient

# Set your API ID, API hash, and phone number with country code
api_id = '28558549'
api_hash = '7aa7cc23963372ec5bcd5baf56d9817e'
phone_number = '+2348120541489'

# Set the source and destination group IDs
source_group_id = -1001256233087  # Replace with your source group ID
destination_group_id = -4177542637  # Replace with your destination group ID

# Create a new TelegramClient instance
client = TelegramClient('session_name', api_id, api_hash)

# Start the client
client.start(phone=phone_number)
print('Client started successfully!')

# Transfer members from the source group to the destination group
async def transfer_members(limit=None):
    count = 0
    async for participant in client.iter_participants(source_group_id):
        # Add each participant to the destination group
        try:
            await client.get_entity(destination_group_id).add_user(participant.id)
            print(f"Transferred user {participant.id} to the destination group.")
            count += 1

            if limit is not None and count >= limit:
                print(f"Scrapped {limit} members as requested.")
                break

        except Exception as e:
            print(f"Failed to transfer user {participant.id}: {e}")

# Run the transfer_members coroutine
with client:
    command = input("Enter a command (/scrap, /scrap <limit>, or 'stop'): ")

    if command.startswith('/scrap'):
        if command == '/scrap':
            client.loop.run_until_complete(transfer_members())
        else:
            try:
                limit = int(command.split()[1])
                client.loop.run_until_complete(transfer_members(limit))
            except ValueError:
                print("Invalid limit provided. Please provide a number.")
    elif command == 'stop':
        print("Scraping stopped.")
