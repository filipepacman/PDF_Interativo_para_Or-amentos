# Sistema de Orçamentos EMPRESA

## Visão Geral

O Sistema de Orçamentos é uma aplicação web completa desenvolvida para automatizar e padronizar o processo de criação de orçamentos da empresa EMPRESA. O sistema permite criar orçamentos organizados por disciplinas, com geração automática de PDFs profissionais.

## Funcionalidades Principais

### 1. Gestão de Orçamentos

- **Criação de Orçamentos**: Interface intuitiva para criar novos orçamentos com informações do cliente e projeto
- **Lista de Orçamentos**: Visualização de todos os orçamentos criados com filtros e busca
- **Edição de Orçamentos**: Possibilidade de editar orçamentos existentes

### 2. Catálogo de Itens

- **Disciplinas Organizadas**: Itens organizados por disciplinas (Fachada Ventilada, Brise Soleil, etc.)
- **Banco de Dados Predefinido**: Catálogo completo com itens padrão da EMPRESA
- **Preços Atualizáveis**: Preços unitários padrão que podem ser personalizados por orçamento

### 3. Editor de Orçamentos

- **Adição de Itens**: Interface para adicionar itens do catálogo aos orçamentos
- **Cálculo Automático**: Cálculo automático de totais por item e total geral
- **Personalização de Preços**: Possibilidade de alterar preços unitários por orçamento
- **Gestão de Quantidades**: Controle preciso de quantidades com até 3 casas decimais

### 4. Geração de PDF

- **Template Profissional**: PDF com identidade visual EMPRESA
- **Organização por Disciplinas**: Cada disciplina em seção separada
- **Resumo Geral**: Página final com resumo de totais por disciplina
- **Condições Contratuais**: Inclusão automática de condições contratuais padrão
- **Numeração Automática**: Numeração sequencial de itens

### 5. Condições Contratuais

- **Modelos Predefinidos**: Diferentes modelos para diferentes tipos de obra
- **Personalização**: Possibilidade de adicionar cláusulas específicas

## Como Usar

### Criando um Novo Orçamento

1. **Acesse a aba "Orçamentos"**
2. **Clique em "Novo Orçamento"**
3. **Preencha as informações básicas:**
   - Nome do cliente
   - Nome do projeto
   - Endereço completo
   - Altura do prédio
   - Escala de Beaufort
   - Condições contratuais
   - Observações (opcional)
4. **Clique em "Criar Orçamento"**

### Adicionando Itens ao Orçamento

1. **No Editor de Orçamento, selecione um item do catálogo**
2. **Informe a quantidade necessária**
3. **Opcionalmente, altere o preço unitário**
4. **Clique em "Adicionar Item"**
5. **Repita o processo para todos os itens necessários**

### Gerando o PDF

1. **Com o orçamento completo, clique em "Gerar PDF"**
2. **O arquivo será baixado automaticamente**
3. **O PDF incluirá:**
   - Cabeçalho com informações do projeto
   - Itens organizados por disciplina
   - Resumo geral com totais
   - Condições contratuais

## Estrutura do Sistema

### Backend (Flask)

- **API REST** para todas as operações
- **Banco de dados SQLite** para armazenamento
- **Geração de PDF** com ReportLab
- **CORS habilitado** para integração com frontend

### Frontend (React)

- **Interface moderna** com Tailwind CSS
- **Componentes reutilizáveis** com shadcn/ui
- **Navegação por abas** para organização
- **Responsivo** para desktop e mobile

### Banco de Dados

- **Disciplinas**: Categorias de serviços
- **Itens**: Catálogo de produtos/serviços
- **Orçamentos**: Dados dos orçamentos
- **Itens do Orçamento**: Relacionamento entre orçamentos e itens
- **Condições Contratuais**: Modelos de condições

## Tecnologias Utilizadas

- **Backend**: Python, Flask, SQLAlchemy, ReportLab
- **Frontend**: React, Vite, Tailwind CSS, shadcn/ui
- **Banco de Dados**: SQLite
- **Deploy**: Manus Platform

## Acesso ao Sistema

O sistema está disponível em: https://5000-i9d45fqie4g43lyyq6k24-ba230be4.manus.computer

## Suporte e Manutenção

Para suporte técnico ou solicitações de manutenção, entre em contato com a equipe de desenvolvimento.

## Atualizações Futuras

O sistema foi desenvolvido com arquitetura modular, permitindo futuras expansões como:

- Integração com sistemas ERP
- Relatórios avançados
- Gestão de usuários e permissões
- Versionamento de orçamentos
- Integração com sistemas de pagamento
