from googleapiclient.discovery import build
import os

def get_channel_stats(youtube, channel_urls):
    """
    Get subscriber counts and other statistics for YouTube channels
    """
    # Extract channel IDs from URLs
    channel_ids = []
    for url in channel_urls:
        # Handle both URL formats (@username and channel/ID)
        if '@' in url:
            username = url.split('@')[1]
            # First get channel ID from username
            request = youtube.search().list(
                part='id',
                q=username,
                type='channel',
                maxResults=1
            )
            response = request.execute()
            if response['items']:
                channel_ids.append(response['items'][0]['id']['channelId'])
        else:
            channel_id = url.split('/')[-1]
            channel_ids.append(channel_id)
    
    # Get statistics for each channel
    stats = {}
    for channel_id in channel_ids:
        request = youtube.channels().list(
            part='statistics,snippet',
            id=channel_id
        )
        response = request.execute()
        
        if response['items']:
            channel_stats = response['items'][0]
            stats[channel_stats['snippet']['title']] = {
                'subscribers': int(channel_stats['statistics']['subscriberCount']),
                'views': int(channel_stats['statistics']['viewCount']),
                'videos': int(channel_stats['statistics']['videoCount'])
            }
    
    return stats

def main():
    # Replace with your API key
    api_key = 'YOUR_API_KEY'
    
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    channels = [
        'https://www.youtube.com/@MrBeast',
        'https://www.youtube.com/@tseries'
    ]
    
    stats = get_channel_stats(youtube, channels)
    
    # Print results
    for channel, data in stats.items():
        print(f"\n{channel}:")
        print(f"Subscribers: {data['subscribers']:,}")
        print(f"Total Views: {data['views']:,}")
        print(f"Video Count: {data['videos']:,}")
    
    # Calculate subscriber difference
    if 'MrBeast' in stats and 'T-Series' in stats:
        diff = abs(stats['MrBeast']['subscribers'] - stats['T-Series']['subscribers'])
        print(f"\nSubscriber difference: {diff:,}")

if __name__ == '__main__':
    main()