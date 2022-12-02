#!/usr/bin/python
# createManagedServer.py

import time
import getopt
import sys
import re

# Localizar o arquivo properties

properties = ''
try:
    opts, args = getopt.getopt(sys.argv[1:], "p:h::", ["properties="])
except getopt.GetoptError:
    print "createManagedServer.py -p"
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print "createManagedServer.py -p"
        sys.exit()
    elif opt in ('-p', '--properties'):
        properties = arg
print "properties=", properties

# Carrega as informacoes do arquivo properties

from java.io import FileInputStream

propInputStream = FileInputStream(properties)
configProps = Properties()
configProps.load(propInputStream)

# Atribuicao de variaveis e seus respectivos valores

adminUsername = configProps.get("admin.username")
adminPassword = configProps.get("admin.password")
adminURL = configProps.get("admin.url")
managedServerName = configProps.get("ms.name")
managedServerAddress = configProps.get("ms.address")
managedServerPort = configProps.get("ms.port")
managedServerCluster = configProps.get("ms.cluster")
managedServerSSLPort = configProps.get("ms.sslport")
managedServerMachine = configProps.get("ms.machine")

# Mostrar valores atribuidos as variaveis

print 'adminUsername =', adminUsername
print 'adminPassword=', adminPassword
print 'adminURL=', adminURL
print 'managedServerName=', managedServerName
print 'managedServerAddress=', managedServerAddress
print 'managedServerPort=', managedServerPort
print 'managedServerMachine=', managedServerMachine

# Conectar ao admin console

connect(adminUsername, adminPassword, adminURL)

edit()
startEdit()

# Criar o managed server

cd('/')
cmo.createServer(managedServerName)
cd('/Servers/' + managedServerName)
cmo.setListenAddress(managedServerAddress)
cmo.setListenPort(int(managedServerPort))

# Criar um cluster

cd('/')
cmo.createCluster(managedServerCluster)

cd('/Clusters/' + managedServerCluster)
cmo.setClusterMessagingMode('unicast')
cmo.setClusterBroadcastChannel('')
#cmo.setClusterAddress(clusterAddress)

# Associar managed server a um cluster

if managedServerCluster:
  cd('/Servers/' + managedServerName)
  cmo.setCluster(getMBean('/Clusters/' + managedServerCluster))

# Definir saida padrao (stdout) e escrita de erro padrao (stderr)

cd('/Servers/' + managedServerName + '/Log/' + managedServerName)
cmo.setRedirectStderrToServerLogEnabled(true)
cmo.setRedirectStdoutToServerLogEnabled(true)
cmo.setMemoryBufferSeverity('Debug')

# Associar o managed server ao node manager

cd('/Servers/' + managedServerName)
cmo.setMachine(getMBean('/Machines/' + managedServerMachine))

# Configurar rotate dos logs do managed server

cd('/Servers/' + managedServerName + '/Log/' + managedServerName)
cmo.setRotationType('byTime')
cmo.setFileCount(30)
cmo.setRedirectStderrToServerLogEnabled(true)
cmo.setRedirectStdoutToServerLogEnabled(true)
cmo.setMemoryBufferSeverity('Debug')
cmo.setLogFileSeverity('Notice')

save()
activate()

disconnect()
exit()
