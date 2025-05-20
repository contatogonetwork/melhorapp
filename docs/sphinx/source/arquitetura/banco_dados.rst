==============
Banco de Dados
==============

Estrutura do Banco de Dados
--------------------------

O GoNetwork AI utiliza um banco de dados SQLite para armazenar todas as informações do sistema.
O arquivo do banco de dados está localizado em ``data/gonetwork.db``.

Principais Tabelas
-----------------

A estrutura do banco de dados inclui as seguintes tabelas principais:

Usuários e Equipe
~~~~~~~~~~~~~~~~

* **users**: Armazena informações de usuários do sistema
* **team_members**: Membros da equipe que trabalham nos eventos
* **event_team_members**: Associação entre eventos e membros da equipe

Eventos e Clientes
~~~~~~~~~~~~~~~~

* **events**: Eventos gerenciados pelo sistema
* **clients**: Informações de clientes
* **sponsors**: Patrocinadores de eventos

Briefing
~~~~~~~

* **briefings**: Briefings para eventos
* **stages**: Palcos para eventos
* **attractions**: Atrações para cada palco

Timeline
~~~~~~~

* **timeline_items**: Itens do cronograma de eventos
* **timeline_milestones**: Marcos importantes no cronograma
* **timeline_notifications**: Notificações relacionadas ao cronograma

Edição de Vídeo
~~~~~~~~~~~~~~

* **videos**: Informações sobre vídeos
* **video_cuts**: Cortes de vídeo
* **video_comments**: Comentários sobre vídeos
* **video_tags**: Tags para classificação de vídeos

Diagrama Entidade-Relacionamento
------------------------------

.. image:: ../_static/images/diagrama_er.png
   :alt: Diagrama Entidade-Relacionamento
   :width: 800px

*Nota: A imagem acima é uma representação simplificada das principais entidades e relacionamentos.*

Índices e Otimização
------------------

Para garantir um desempenho adequado, o banco de dados possui índices nas seguintes colunas:

* **events**: id, client_id, start_date
* **team_members**: id, role
* **clients**: id, company
* **briefings**: event_id
* **sponsors**: briefing_id
* **timeline_items**: event_id, responsible_id, status
* **videos**: event_id, status

Manutenção
---------

O sistema inclui scripts para manutenção do banco de dados:

* ``check_database_integrity.py``: Verifica a integridade do banco de dados
* ``optimize_database.py``: Cria índices e otimiza o desempenho
