from tap_copper.streams.base import BaseStream
import singer

LOGGER = singer.get_logger()


class CustomFieldsStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'custom_fields'
    KEY_PROPERTIES = ['id']

        
    @property
    def path(self):
        return '/custom_field_definitions'

    def sync_data(self):
        table = self.TABLE

        LOGGER.info('Syncing data for {}'.format(table))
        url = self.get_url()
    
        response = self.client.make_request(url, self.API_METHOD)
        transformed = self.get_stream_data(response)

        with singer.metrics.record_counter(endpoint=table) as counter:
            singer.write_records(table, transformed)
            counter.increment(len(transformed))

        LOGGER.info('Synced {}'.format(table))
                
        return self.state   