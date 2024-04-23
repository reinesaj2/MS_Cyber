import logging
import sys
import collections
from collections import OrderedDict

#
# pip install python-evtx
#
import Evtx.Evtx as evtx

#
# For more information, check 
#      https://chapinb.com/python-forensics-handbook/ch03_event_logs.html
#      https://github.com/chapinb/python-forensics-handbook
#
def open_evtx(input_file):
    """Opens a Windows Event Log and displays common log parameters.

    Arguments:
        input_file (str): Path to evtx file to open

    Examples:
        >>> open_evtx("System.evtx")
        File version (major): 3
        File version (minor): 1
        File is ditry: True
        File is full: False
        Next record number: 10549
    """

    with evtx.Evtx(input_file) as open_log:
        header = open_log.get_file_header()
        properties = OrderedDict(
            [
                ("major_version", "File version (major)"),
                ("minor_version", "File version (minor)"),
                ("is_dirty", "File is dirty"),
                ("is_full", "File is full"),
                ("next_record_number", "Next record number"),
            ]
        )

        for key, value in properties.items():
            print(f"{value}: {getattr(header, key)()}")

def get_events(input_file, parse_xml=False):
    """Opens a Windows Event Log and returns XML information from
    the event record.

    Arguments:
        input_file (str): Path to evtx file to open
        parse_xml (bool): If True, return an lxml object, otherwise a string

    Yields:
        (generator): XML information in object or string format

    Examples:
        >>> for event_xml in enumerate(get_events("System.evtx")):
        >>>     print(event_xml)

    """
    with evtx.Evtx(input_file) as event_log:
        for record in event_log.records():
            if parse_xml:
                yield record.lxml()
            else:
                yield record.xml()

def filter_events_json(event_data, event_ids, fields=None):
    """Provide events where the event id is found within the provided list
    of event ids. If found, it will return a JSON formatted object per event.

    If a list of fields are provided, it will filter the resulting JSON event
    object to contain only those fields.

    Arguments:
        event_data (genertor): Iterable containing event data as XML. Preferably
            the result of the :func:`get_events()` method.
        event_ids (list): A list of event identifiers. Each element should be a
            string value, even though the identifier is an integer.
        fields (list): Collection of fields from the XML data to include in the
            JSON output. Only supports top-level fields.

    Yields:
        (dict): A dictionary containing the filtered record information

    Example:

        >>> filtered_logins = filter_events_json(
        >>>     get_events("System.evtx", parse_xml=True),
        >>>     event_ids=['4624', '4625'],
        >>>     fields=["SubjectUserName", "SubjectUserSid",
        >>>             "SubjectDomainName", "TargetUserName", "TargetUserSid",
        >>>             "TargetDomainName", "WorkstationName", "IpAddress",
        >>>             "IpPort", "ProcessName"]
        >>> )
        >>> for filtered_login in filtered_logins:
        >>>     print(json.dumps(filtered_login, indent=2))

    """
    for evt in event_data:
        system_tag = evt.find("System", evt.nsmap)
        event_id = system_tag.find("EventID", evt.nsmap)
        if event_id.text in event_ids:
            event_data = evt.find("EventData", evt.nsmap)
            json_data = {}
            for data in event_data.getchildren():
                if not fields or data.attrib["Name"] in fields:
                    # If we don't have a specified field filter list, print all
                    # Otherwise filter for only those fields within the list
                    json_data[data.attrib["Name"]] = data.text

            yield json_data

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Use python winevents.py FILENAME")
    else:
        open_evtx(sys.argv[1])
        # for event_xml in enumerate(get_events(sys.argv[1])):
        #    print(event_xml)
        with evtx.Evtx(sys.argv[1]) as event_log:
            for record in event_log.records():
                try:
                    print (record.xml())
                except Exception as e:
                    print("Error: ", e)
