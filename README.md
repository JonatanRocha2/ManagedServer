# Playbook para criação de cluster, data source e managed servers

Automatização de criacao de cluster, managed servers e data sources usando scripts em python executados pelo `WLST`.

## Lembretes para executar este playbook
#### Como funcionam os scripts

Os scripts são templates disponibilizados pela Oracle para automatizar vários recursos do `WebLogic`.
Ao serem invocados pelo `WLST` deverá ser usado um arquivo `.properties` com as informações que serão usadas.

Exemplo:

```shell
# AdminServer connection details.
admin.username=weblogic
admin.password=Password1
admin.url=t3://ol6.localdomain:7001

ms.name=myServer_1
ms.address=ol6.localdomain
ms.port=7002
ms.cluster=myCluster_1
ms.sslport=7502
ms.machine=ol6.localdomain
```

### Como são executados os scripts manualmente

```shell
# Create the managed servers.
java weblogic.WLST <file/to/path>create_managed_server.py -p <file/to/path>myDomain-ms1.properties
java weblogic.WLST <file/to/path>create_managed_server.py -p <file/to/path>myDomain-ms2.properties
```

### Ordem da criação da infraestrutura no weblogic:

1. Cluster

2. Managed server

3. Data source

### Variáveis

A playbook executa de forma interativa, todas as variáveis são passadas na execução.

### Tags

Foram adicionadas `tags` para executar a criação da infraestrutura separada, de acordo com a necessidade.
As `tags` deverão ser informadas no final do comando de execução, usando a flag `--tags=`.
Os valores possíveis são: 

- server (Apenas cria os manageds servers);
- cluster (Apenas cria o cluster);
- ds (Apenas cria o data source);
- sysctl (Apenas configura o start/stop dos manageds servers no `systemctl`).

### Cuidados e observações

1. Os alvos deverão ser definidos no arquivo `hosts` na raiz do projeto;
2. Ao final da execução, o novo managed server será iniciado;
3. Para start/stop dos mangeds servers, dê preferência usando o `systemctl start|stop|status nome-do-managed`;
4. Caso retorne falha na primeira execurção deste playbook, repita usando o comando `ansible-playbook -i hosts main.yml --tags=sysctl -e "domain_name=nome-do-dominio ms_name=nome-do-managed admin_console_ip=ip-do-admin-console"`;
5. Use a opção `-vvv` para vizualizar os logs da execução e encontrar possíveis erros;
6. Verifique se o novo managed server terá um data source criado, se não use a opção `--skip-tags=ds` ao final do comando de execução.

### Exemplo de execução

```shell
git clone git@gitlab.sefa.pa.gov.br:ansible/ManagedServer.git
cd ManagedServer/
ansible-playbook -i hosts main.yml
```
