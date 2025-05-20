# Melhorias de Acessibilidade no GoNetwork AI

Este documento descreve as melhorias de acessibilidade implementadas no aplicativo GoNetwork AI para garantir que o sistema seja utilizável por pessoas com diferentes necessidades.

## Recursos Implementados

### 1. Ajuste de Tamanho de Fonte

O sistema permite que os usuários ajustem o tamanho da fonte em toda a aplicação, com quatro níveis disponíveis:
- Pequeno (85% do tamanho normal)
- Normal (tamanho padrão)
- Grande (125% do tamanho normal)
- Extra Grande (150% do tamanho normal)

O tamanho da fonte pode ser ajustado através do menu de acessibilidade ou usando os atalhos de teclado:
- `Ctrl+F` - Aumentar tamanho da fonte
- `Ctrl+Shift+F` - Diminuir tamanho da fonte

### 2. Esquemas de Cores Acessíveis

Os seguintes esquemas de cores estão disponíveis:

#### Normal
Usa o esquema de cores padrão do sistema.

#### Alto Contraste
Projetado para usuários com baixa visão, usando:
- Fundo preto
- Texto branco
- Bordas destacadas
- Contraste otimizado para elementos interativos

#### Modo Escuro
Reduz a fadiga visual com:
- Fundo escuro (#2d2d2d)
- Texto claro (#e0e0e0)
- Menos brilho para uso noturno

#### Modo Claro
Esquema de cores claro otimizado com contraste adequado.

### 3. Suporte para Leitores de Tela

O modo para leitores de tela melhora a compatibilidade com tecnologias assistivas:
- Configuração adequada de nomes e descrições acessíveis
- Ordem de tabulação lógica
- Foco visual aprimorado
- Feedback adequado para ações

### 4. Navegação por Teclado

O aplicativo pode ser operado completamente por teclado:
- Navegação entre controles com Tab
- Atalhos de teclado para funções comuns
- Indicadores visuais claros do foco atual
- Suporte para teclas de atalho personalizadas

## Como Usar

### Widget de Configurações de Acessibilidade

O widget `AccessibilitySettingsWidget` pode ser integrado em qualquer parte do aplicativo e oferece uma interface para ajustar todas as opções de acessibilidade.

### Classe AccessibilityManager

A classe `AccessibilityManager` é um singleton que gerencia as configurações de acessibilidade em toda a aplicação:

```python
from utils.accessibility import AccessibilityManager, FontSize, ColorScheme

# Obter a instância do gerenciador
manager = AccessibilityManager()

# Ajustar tamanho da fonte
manager.set_font_size(FontSize.LARGE)

# Aplicar esquema de alto contraste
manager.set_color_scheme(ColorScheme.HIGH_CONTRAST)

# Ativar modo para leitores de tela
manager.set_screen_reader_mode(True)
```

### Funções Utilitárias

```python
from utils.accessibility import make_widget_accessible, add_keyboard_shortcut

# Tornar um widget acessível
make_widget_accessible(
    my_button,
    "Salvar alterações",
    "Botão para salvar as alterações feitas no formulário"
)

# Adicionar atalho de teclado
add_keyboard_shortcut(
    my_widget,
    "Ctrl+S",
    save_function
)
```

## Demonstração

O script `accessibility_demo.py` demonstra todos os recursos de acessibilidade implementados. Execute-o para ver as funcionalidades em ação:

```bash
python accessibility_demo.py
```

## Boas Práticas de Acessibilidade

Ao desenvolver novos recursos para o GoNetwork AI, siga estas diretrizes:

1. **Texto Alternativo**: Forneça textos alternativos para todas as imagens e ícones.

2. **Contraste de Cores**: Mantenha um contraste mínimo de 4.5:1 entre texto e fundo.

3. **Tamanho de Fonte**: Use unidades relativas em vez de absolutas.

4. **Navegação por Teclado**: Garanta que todas as funcionalidades sejam acessíveis por teclado.

5. **Nomes Acessíveis**: Forneça nomes acessíveis significativos para todos os widgets.

6. **Descrições**: Adicione descrições para explicar o propósito de elementos complexos.

7. **Feedback**: Forneça feedback visual e auditivo para ações importantes.

8. **Simplificação**: Mantenha a interface simples e intuitiva.

## Testes de Acessibilidade

Para garantir que o aplicativo seja realmente acessível, teste-o regularmente:

1. Use o aplicativo apenas com o teclado
2. Teste com leitores de tela (NVDA, JAWS, VoiceOver)
3. Verifique o contraste de cores
4. Teste com diferentes tamanhos de fonte

## Referências

- [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/standards-guidelines/wcag/)
- [Qt Accessibility](https://doc.qt.io/qt-6/accessible.html)
