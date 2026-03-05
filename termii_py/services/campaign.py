"""
This module provides the CampaignService class, which allows you to send SMS campaigns, fetch campaign details, and
retry failed campaigns using the Termii API. The service includes methods to send campaigns with various options such
as scheduling, link tracking, and channel selection. It also provides functionality to retrieve campaign history and
 retry campaigns that may have failed.

References:
    - https://developer.termii.com/campaign

Classes:
    CampaignService: A service class that provides methods to manage SMS campaigns via Termii's API
"""
from termii_py.http import RequestHandler


class CampaignService:
    """
    Provides methods to manage SMS campaigns through Termii's API. The class includes methods to send SMS campaigns
    with various options, fetch campaign details, and retry failed campaigns. Each method constructs the appropriate
    API request and handles the response.

    Attributes:
        http (object): An HTTP client instance responsible for making API requests to Termii.
    """

    def __init__(self, http: RequestHandler):
        """
        Initializes the CampaignService instance. This constructor takes an HTTP client instance as an argument, which
        is used to perform network requests to the Termii API.

        Args:
            http (object): An HTTP client instance (e.g., `requests.Session`) used to perform network requests to the Termii API.
        """

        self.http = http

    def send_campaign(self, country_code: str, sender_id: str, message: str, message_type: str, phonebook_id: str,
                      enable_link_tracking: bool, campaign_type: str, schedule_sms_status: str,
                      schedule_time: str = None, channel: str = "dnd"):
        """
            Sends an SMS campaign using the Termii API. This method constructs a payload with the provided parameters
            and sends a POST request to the `/api/sms/campaigns/send` endpoint. The method includes validation for the
            input parameters to ensure they meet the required criteria before making the API call.

            Args:
                country_code (str): The country code for the recipients of the campaign (e.g., "234" for Nigeria).
                sender_id (str): The sender ID to be displayed on the recipient's device (must be between 3 and 11 characters).
                message (str): The content of the SMS message to be sent in the campaign.
                message_type (str): The type of message, either "plain" for standard text or "unicode" for messages containing special characters.
                phonebook_id (str): The unique identifier of the phonebook containing the recipients of the campaign.
                enable_link_tracking (bool): A flag indicating whether link tracking should be enabled for the campaign.
                campaign_type (str): The type of campaign, which can be "promotional" or "transactional".
                schedule_sms_status (str): The scheduling status of the campaign, either "scheduled" for campaigns that should be sent at a later time or "regular" for immediate sending.
                schedule_time (str, optional): The scheduled time for the campaign to be sent, required if `schedule_sms_status` is "scheduled". The format should be in ISO 8601 (e.g., "2024-12-31T23:59:00Z").
                channel (str, optional): The channel through which the campaign should be sent, either "dnd" for Do Not Disturb compliant messages or "generic" for standard messages. Default is "dnd".

            Raises:
                ValueError: If any of the input parameters do not meet the required criteria (e.g., invalid country code,
                sender ID length, message type, campaign type, scheduling status, or missing schedule time when required).

            Returns:
                A response object containing the result of the campaign send operation, including status and any relevant metadata

            References:
                - https://developer.termii.com/campaign#:~:text=a%20specified%20phonebook.-,Send%20a%20campaign,-This%20endpoint%20allows
        """

        if country_code.startswith("+"):
            raise ValueError("country code should not start with '+' sign.")

        if len(sender_id) < 3 or len(sender_id) > 11:
            raise ValueError("sender id should be between 3 and 11 characters.")

        if message_type not in ["plain", "unicode"]:
            raise ValueError("message type should be either 'plain' or 'unicode'.")

        if channel not in ["dnd", "generic"]:
            raise ValueError("channel should be either 'dnd' or 'generic'.")

        if schedule_sms_status not in ["scheduled", "regular"]:
            raise ValueError("schedule sms status should be either 'scheduled' or 'regular'.")

        if schedule_sms_status == "scheduled" and not schedule_time:
            raise ValueError("schedule time is required when schedule sms status is 'scheduled'.")

        payload = {
            "country_code": country_code,
            "sender_id": sender_id,
            "message": message,
            "message_type": message_type,
            "phonebook_id": phonebook_id,
            "enable_link_tracking": enable_link_tracking,
            "campaign_type": campaign_type,
            "schedule_sms_status": schedule_sms_status,
            "schedule_time": schedule_time,
            "channel": channel,
            "remove_duplicate": "yes",
            "delimiter": ","
        }

        return self.http.post("/api/sms/campaigns/send", payload)

    def fetch_campaigns(self):
        """
            Fetches a list of all SMS campaigns that have been sent or are scheduled to be sent using the Termii
            API. This method sends a GET request to the `/api/sms/campaigns` endpoint and retrieves the campaign
            history, including details such as campaign ID, status, message content, recipient information, and
            scheduling details. The response will contain an array of campaign objects, each representing a
            specific campaign with its associated metadata.

            Returns:
                A response object containing a list of SMS campaigns, including details such as campaign ID, status,
                message content, recipient information, and scheduling details.

            References:
                - https://developer.termii.com/campaign#fetch-campaigns:~:text=C714360330258%22%2C%0A%20%20%20%20%22status%22%3A%20%22success%22%0A%20%20%7D-,Fetch%20campaigns,-This%20endpoint%20retrieves
        """

        return self.http.fetch("/api/sms/campaigns")

    def fetch_campaign_history(self, campaign_id: str):
        """
            Fetches the details of a specific SMS campaign using its unique identifier (campaign ID). This method sends
            a GET request to the `/api/sms/campaigns/{campaign_id}` endpoint, where `{campaign_id}` is the unique
            identifier of the campaign whose details you want to retrieve. The response will contain comprehensive
            information about the specified campaign, including its status, message content, recipient
            information, scheduling details, and any relevant metadata.

            Args:
                campaign_id (str): The unique identifier of the SMS campaign for which to fetch details. This ID is
                typically returned when a campaign is created or can be obtained from the list of campaigns.

            Raises:
                ValueError: If the `campaign_id` is not provided or is invalid. The campaign ID is required to fetch
                the details of a specific campaign, and it must be a valid identifier that exists in the system.

            Returns:
                A response object containing the details of the specified SMS campaign, including its status, message
                content, recipient information, scheduling details, and any relevant metadata.
        """

        if not campaign_id:
            raise ValueError("campaign id is required")

        return self.http.fetch(f"/api/sms/campaigns/{campaign_id}")

    def retry_campaign(self, campaign_id: str):
        """
            Retries a specific SMS campaign that may have failed or encountered issues during its initial sending attempt.
            This method sends a PATCH request to the `/api/sms/campaigns/{campaign_id}` endpoint, where `{campaign_id}`
            is the unique identifier of the campaign you wish to retry. The response will indicate whether the retry
            attempt was successful and may include updated campaign details or status information. This functionality
            is useful for campaigns that may have failed due to temporary issues such as network errors or recipient
            device problems, allowing you to attempt sending the campaign again without having to create a new one.

            Args:
                campaign_id (str): The unique identifier of the SMS campaign that you want to retry. This ID is typically
                returned when a campaign is created or can be obtained from the list of campaigns. It must be a valid
                identifier corresponding to an existing campaign in the system.

            Raises:
                ValueError: If the `campaign_id` is not provided or is invalid. The campaign ID is required to identify
                which campaign to retry, and it must be a valid identifier that exists in the system.

            Returns:
                A response object indicating the result of the retry attempt, including whether it was successful and
                any relevant details about the campaign's updated status or information.
        """

        if not campaign_id:
            raise ValueError("campaign id is required")

        payload = {}

        return self.http.patch(f"/api/sms/campaigns/{campaign_id}", json=payload)
