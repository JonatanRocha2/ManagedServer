#!/usr/bin/python
# Save Script as : create_managed_server.py

import time
import getopt
import sys
import re

# # localiza o arquivo properties.
# properties = ''
# try:
#    opts, args = getopt.getopt(sys.argv[1:],"p:h::",["properies="])
# except getopt.GetoptError:
#    print 'create_managed_server.py -p <path-to-properties-file>'
#    sys.exit(2)
# for opt, arg in opts:
#    if opt == '-h':
#       print 'create_managed_server.py -p <path-to-properties-file>'
#       sys.exit()
#    elif opt in ("-p", "--properties"):
#       properties = arg
# print 'properties=', properties


from java.io import FileInputStream


propInputStream = FileInputStream(properties)
configProps = Properties()
configProps.load(propInputStream)


# Seta variaveis a partir do properties.
adminUsername=configProps.get("admin.username")
adminPassword=configProps.get("admin.password")
adminURL=configProps.get("admin.url")
#msName=configProps.get("ms.name")
msAddress1=configProps.get("ms.address01")
msAddress2=configProps.get("ms.address02")
msPort=configProps.get("ms.port")
msCluster=configProps.get("ms.cluster")
#msSSLPort=configProps.get("ms.sslport")
msMachine01=configProps.get("ms.machine01")
msMachine02=configProps.get("ms.machine02")



#Seta variavel local
msName01 = (msCluster + '01')
msName02 = (msCluster + '02')
Dsource = (msCluster + 'DS')



# Display the variable values.
#print 'adminUsername=', adminUsername
#print 'adminPassword=', adminPassword
print 'adminURL=', adminURL
#print 'msName=', msName
print 'msAddress1=', msAddress1
print 'msAddress2=', msAddress2
print 'msPort=', msPort
print 'msCluster=', msCluster
#print 'msSSLPort=', msSSLPort
#print 'msMachine=', msMachine
print 'msName01',msName01
print 'msName02',msName02
print 'Dsource',Dsource



# Conecta ao admin server.
connect(adminUsername, adminPassword, adminURL)
edit()
startEdit()



# Cria o managed Server01.
cd('/')
cmo.createServer(msName01)
cd('/Servers/' + msName01)
cmo.setListenAddress(msAddress1)
cmo.setListenPort(int(msPort))
cmo.getWebServer().setMaxRequestParamterCount(25000)



# Direct stdout and stderr.
cd('/Servers/' + msName01 + '/Log/' + msName01)
cmo.setRedirectStderrToServerLogEnabled(true)
cmo.setRedirectStdoutToServerLogEnabled(true)
cmo.setMemoryBufferSeverity('Debug')



# Cria o managed Server02.
cd('/')
cmo.createServer(msName02)
cd('/Servers/' + msName02)
cmo.setListenAddress(msAddress2)
cmo.setListenPort(int(msPort))
cmo.getWebServer().setMaxRequestParamterCount(25000)


# Direct stdout and stderr.
cd('/Servers/' + msName02 + '/Log/' + msName02)
cmo.setRedirectStderrToServerLogEnabled(true)
cmo.setRedirectStdoutToServerLogEnabled(true)
cmo.setMemoryBufferSeverity('Debug')


# Vincula template
cd('/Servers/'+ msName01)
cmo.setServerTemplate(getMBean('/ServerTemplates/ServerTemplate-256m'))
cmo.isInherited('Machine')
cmo.isInherited('Cluster')


cd('/Servers/'+ msName02)
cmo.setServerTemplate(getMBean('/ServerTemplates/ServerTemplate-256m'))
cmo.isInherited('Machine')
cmo.isInherited('Cluster')


#Cria o Clusters
cd('/')
cmo.createCluster(msCluster)
cd('/Clusters/'+ msCluster)
cmo.setClusterMessagingMode('unicast')
cmo.setClusterBroadcastChannel('')


# Associa a um cluster.
cd('/Servers/' + msName01)
cmo.setCluster(getMBean('/Clusters/' + msCluster))
cd('/Servers/' + msName02)
cmo.setCluster(getMBean('/Clusters/' + msCluster))


# Habilita SSL e vincula .
#cd('/Servers/' + msName + '/SSL/' + msName)
#cmo.setEnabled(true)
#cmo.setListenPort(int(msSSLPort))


# Associa a um node manager.
cd('/Servers/' + msName01)
cmo.setMachine(getMBean('/Machines/' + msMachine01))

cd('/Servers/' + msName02)
cmo.setMachine(getMBean('/Machines/' + msMachine02))



# Build any data sources later.
cd('/Servers/' + msName01 + '/DataSource/' + msName01)
cmo.setRmiJDBCSecurity(None)



cd('/Servers/' + msName02 + '/DataSource/' + msName02)
cmo.setRmiJDBCSecurity(None)



# Manage logging.
cd('/Servers/' + msName01 + '/Log/' + msName01)
cmo.setRotationType('byTime')
cmo.setFileCount(30)
cmo.setRedirectStderrToServerLogEnabled(true)
cmo.setRedirectStdoutToServerLogEnabled(true)
cmo.setMemoryBufferSeverity('Debug')
cmo.setLogFileSeverity('Notice')



cd('/Servers/' + msName02 + '/Log/' + msName02)
cmo.setRotationType('byTime')
cmo.setFileCount(30)
cmo.setRedirectStderrToServerLogEnabled(true)
cmo.setRedirectStdoutToServerLogEnabled(true)
cmo.setMemoryBufferSeverity('Debug')
cmo.setLogFileSeverity('Notice')



cd('/')
cmo.createJDBCSystemResource('Dsource')
cd('/JDBCSystemResources/'+ Dsource +'/JDBCResource/'+ Dsource)
cmo.setName(Dsource)
cd('/JDBCSystemResources/'+ Dsource +'/JDBCResource/'+ Dsource +'/JDBCDataSourceParams/'+ Dsource)
set('JNDINames',jarray.array([String('jdbc/'+ Dsource)], String))
cd('/JDBCSystemResources/'+ Dsource +'/JDBCResource/'+ Dsource +'/JDBCDriverParams/'+ Dsource)
cmo.setUrl('jdbc:oracle:thin:@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=exa01-scan.sefa.pa.gov.br)(PORT=1521)))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=apps_extranet.sefa.pa.gov.br)))\r\n\r\n')
cmo.setDriverName('oracle.jdbc.OracleDriver')



#setEncrypted('Password', 'Password_1549544457035', '/u01/Middleware/user_projects/domains/app-pub-extranet.sefa.pa.gov.br/Script1549544138731Config', '/u01/Middleware/user_projects/domains/app-pub-extranet.sefa.pa.gov.br/Script1549544138731Secret')
#cd('/JDBCSystemResources/OuvidoriaDS/JDBCResource/OuvidoriaDS/JDBCConnectionPoolParams/OuvidoriaDS')
#cmo.setTestTableName('SQL ISVALID\r\n\r\n')



#cd('/JDBCSystemResources/'+ Dsource +'/JDBCResource/'+ Dsource +'/JDBCDriverParams/'+ Dsource +'/Properties/'+ Dsource +'')
#cmo.createProperty('user')



#cd('/JDBCSystemResources/OuvidoriaDS/JDBCResource/OuvidoriaDS/JDBCDriverParams/OuvidoriaDS/Properties/OuvidoriaDS/Properties/user')
#cmo.setValue('usr_Ouvidoria')



cd('/JDBCSystemResources/'+ Dsource +'/JDBCResource/'+ Dsource +'/JDBCDataSourceParams/'+ Dsource)
cmo.setGlobalTransactionsProtocol('OnePhaseCommit')



cd('/JDBCSystemResources/'+ Dsource +'/JDBCResource/'+ Dsource)
cmo.setDatasourceType('AGL')



cd('/JDBCSystemResources/'+ Dsource +'/JDBCResource/'+ Dsource +'/JDBCOracleParams/'+ Dsource)
cmo.setFanEnabled(true)
cmo.setOnsWalletFile('')
cmo.setActiveGridlink(true)
cmo.unSet('OnsWalletPasswordEncrypted')
cmo.setOnsNodeList('')
cmo.setFanEnabled(true)
cmo.setOnsWalletFile('')
cmo.setActiveGridlink(true)



cd('/JDBCSystemResources/'+ Dsource +'/JDBCResource/'+ Dsource)
cmo.setDatasourceType('AGL')



cd('/JDBCSystemResources/'+ Dsource +'/JDBCResource/'+ Dsource +'/JDBCOracleParams/'+ Dsource)
cmo.unSet('OnsWalletPasswordEncrypted')
cmo.setOnsNodeList('')



cd('/JDBCSystemResources/'+ Dsource)
set('Targets',jarray.array([ObjectName('com.bea:Name=Cluster,Type=Cluster')], ObjectName))




save()
activate()



disconnect()
exit()