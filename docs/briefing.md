# -*- coding: utf-8 -*-
"""
Documentação da Aba Briefing

## Visão Geral

A aba Briefing permite a centralização estratégica completa de todos os aspectos
relacionados a eventos audiovisuais. Ela serve como fonte principal de informações
para as outras abas do sistema, incluindo Timeline, Edições, Entregas e Equipe.

## Principais Recursos

### 1. Informações Gerais e Estilo

- **Informações Gerais**: Campo para descrição abrangente do evento, público-alvo, objetivos, etc.
- **Estilo e Referências**: Local para definir a identidade visual e referências para edições.

### 2. Patrocinadores

Gerenciamento dinâmico de ações de patrocinadores, incluindo:
- Nome da ação
- Horário da captação (fixo ou livre)
- Responsável pela captação
- Opção de entrega em tempo real
- Editor responsável (para entregas em tempo real)
- Orientações específicas

### 3. Programação de Palcos

Tabela para gerenciar programação de atrações em diferentes palcos:
- Nome do palco
- Nome do artista/atração
- Horário de início e fim
- Observações específicas

### 4. Entregas

#### Entregas em Tempo Real
- Título da entrega
- Horário previsto
- Editor responsável
- Plataforma de destino
- Orientações específicas

#### Entregas Pós-Evento
- Deadline geral para todas as entregas
- Pacotes de entrega (Aftermovie, Highlights, Teaser, etc.)
- Observações gerais para entregas pós-evento

## Fluxo de Trabalho

1. Selecione um evento no seletor no topo da tela
2. Preencha as informações das diferentes seções do briefing
3. Salve o briefing usando o botão "Salvar Briefing"
4. Gere uma timeline baseada no briefing usando "Gerar Timeline"

## Integração com Outras Abas

- **Timeline**: Gerada automaticamente a partir dos dados do briefing
- **Edições**: Recebe automaticamente as entregas e editores definidos no briefing
- **Equipe**: Fornece os responsáveis por cada tarefa definida no briefing
- **Entregas**: Utiliza as definições de entregas do briefing para organizar o fluxo de trabalho

## Representação Técnica

O briefing é armazenado no banco de dados nas tabelas:
- `briefings`: Dados gerais do briefing
- `sponsors`: Patrocinadores do evento
- `sponsor_actions`: Ações dos patrocinadores
- `stages`: Palcos do evento
- `attractions`: Atrações programadas para cada palco
- `realtime_deliveries`: Entregas em tempo real
- `post_deliveries`: Entregas pós-evento

## Boas Práticas

- Preencha o briefing o mais detalhadamente possível antes de iniciar o evento
- Atualize o briefing sempre que houver mudanças significativas
- Gere a timeline novamente após alterações importantes no briefing
- Verifique conflitos na aba Timeline após gerar/atualizar a timeline
"""
