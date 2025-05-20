# -*- coding: utf-8 -*-
"""
Documentação da Aba Timeline

## Visão Geral

A aba Timeline oferece uma visualização gráfica das atividades planejadas para um evento,
baseada nos dados definidos no Briefing. Ela permite monitoramento em tempo real,
gerenciamento de conflitos e atualizações de status das atividades.

## Principais Recursos

### 1. Visualização Cronológica

- **Linha do Tempo Visual**: Representação gráfica das atividades por horário
- **Agrupamento por Tipo**: Divisão visual em categorias (captação, edição, entrega, etc.)
- **Cores por Status**: Diferenciação visual de acordo com o status da atividade

### 2. Gerenciamento de Atividades

- **Drag & Drop**: Reposicionamento de atividades na linha do tempo
- **Edição de Detalhes**: Modificação de título, horário, responsável, etc.
- **Atualização de Status**: Alteração rápida para Pendente, Em Andamento, Concluído, etc.

### 3. Ferramentas de Controle

- **Zoom**: Ajuste da escala de tempo para melhor visualização
- **Filtros**: Filtragem por tipo de atividade e responsável
- **Detecção de Conflitos**: Identificação automática de problemas como sobreposição de horários

## Fluxo de Trabalho

1. Selecione um evento no seletor no topo da tela
2. Visualize a timeline gerada a partir do briefing
3. Ajuste posições ou detalhes dos itens conforme necessário
4. Atualize o status das atividades conforme o evento progride
5. Verifique conflitos regularmente para evitar problemas logísticos

## Tipos de Atividades

- **Captação**: Gravações e registros durante o evento
- **Edição**: Processos de edição de conteúdo
- **Entrega**: Momentos de publicação ou entrega de conteúdo
- **Preparação**: Atividades preparatórias ou de organização
- **Outro**: Atividades diversas que não se encaixam nas categorias anteriores

## Status de Atividades

- **Pendente**: Ainda não iniciada
- **Em Andamento**: Iniciada mas não concluída
- **Concluído**: Finalizada com sucesso
- **Atrasado**: Não iniciada ou não concluída após o horário previsto
- **Cancelado**: Não será mais realizada

## Detecção de Conflitos

A timeline detecta automaticamente os seguintes tipos de conflitos:

1. **Sobreposição de Responsáveis**: Quando a mesma pessoa está designada para duas atividades simultâneas
2. **Entrega sem Edição**: Quando há uma entrega programada sem um período de edição anterior correspondente

## Integração com Outras Abas

- **Briefing**: Recebe os dados para geração inicial da timeline
- **Edições**: Fornece prazos e cronograma para o processo de edição
- **Entregas**: Define momentos de entrega e responsáveis
- **Equipe**: Utiliza e informa os responsáveis por cada atividade

## Representação Técnica

A timeline é armazenada no banco de dados nas tabelas:
- `timeline_items`: Itens da timeline (tarefas, entregas, etc.)
- `timeline_milestones`: Marcos importantes da timeline
- `timeline_notifications`: Notificações associadas a itens da timeline
- `timeline_history`: Histórico de alterações na timeline
"""
