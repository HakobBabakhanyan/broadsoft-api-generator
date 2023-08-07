data = """<?xml version="1.0" encoding="ISO-8859-1"?>
<BroadsoftOCIReportingDocument protocol="OCIReporting"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<command xsi:type="OCIReportingReportNotification">
<id>write302082861</id>
<userId>Jazz0872100029@dcihotel.com</userId>
<loginType>Group</loginType>
<request>
<![CDATA[
<?xml version="1.0" encoding="ISO-8859-1"?><BroadsoftDocument protocol="OCI"
            xmlns="C"><userId
            xmlns="">Jazz0872100029@dcihotel.com</userId><command xsi:type="UserOutgoingCallingPlanRedirectingModifyRequest"
            xmlns=""
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><userId>08721000297408@dcihotel.com</userId><useCustomSettings>true</useCustomSettings><userPermissions><group>true</group><local>true</local><tollFree>true</tollFree><toll>true</toll><international>false</international><operatorAssisted>true</operatorAssisted>`
<?xml version="1.0" encoding="ISO-8859-1"?><BroadsoftOCIReportingDocument protocol="OCIReporting"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><command xsi:type="OCIReportingReportNotification"><id>write302082892</id><userId>Jazz0872100029@dcihotel.com</userId><loginType>Group</loginType><request>
<![CDATA[
<?xml version="1.0" encoding="ISO-8859-1"?><BroadsoftDocument protocol="OCI"
            xmlns="C"><userId
            xmlns="">Jazz0872100029@dcihotel.com</userId><command xsi:type="UserOutgoingCallingPlanOriginatingModifyRequest"
            xmlns=""
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><userId>08721000297408@dcihotel.com</userId><useCustomSettings>true</useCustomSettings><userPermissions><group>Allow</group><local>Disallow</local><tollFree>Disallow</tollFree><toll>Disallow</toll><international>Disallow</international><chargeableDirectoryAssisted>Disallow</chargeableDirectoryAssisted><specialServicesI>Disallow</specialServicesI><specialServicesII>Disallow</specialServicesII><premiumServicesI>Disallow</premiumServicesI><urlDialing>Disallow</urlDialing></userPermissions></command></BroadsoftDocument>]]>
</request>
</command>
</BroadsoftOCIReportingDocument>

"""

import xmltodict

xml_dict = xmltodict.parse(data)

# xml_r = xmltodict.parse(xml_dict['BroadsoftOCIReportingDocument']['command']['request'])
print(xml_dict['BroadsoftOCIReportingDocument']['command']['request'])
