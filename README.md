# 🛒 Loja JBS — Sistema Integrado de Gestão Comercial e Frente de Caixa (PDV)

O **Loja JBS** é um ERP e Ponto de Venda (PDV) de alta performance desenvolvido em Python e Django, voltado para automação comercial, gestão financeira flexível e controle rigoroso de estoque e inadimplência.

O sistema conta com interface em **Dark Mode**, painel administrativo customizado com navegação em grid operacional e relatórios interativos em tempo real.

---

## 🚀 Tecnologias Utilizadas

* **Back-end:** Python 3.14+, Django 6.x (Arquitetura orientada a camadas de serviço - Services Layer).
* **Front-end & UI:** HTML5, Tailwind CSS, JavaScript (ES6+), Chart.js (Gráficos interativos).
* **Admin Theme:** Django Unfold (Interface administrativa moderna).
* **Banco de Dados:** SQLite (Desenvolvimento/Testes) e PostgreSQL (Produção/Deploy).
* **Testes & Qualidade:** Pytest, Pytest-Django, Flake8, Coverage.

---

## 📦 Módulos do Sistema

1. **Vendas (Frente de Caixa / PDV):**
   * Carrinho dinâmico com ajuste de quantidade em tempo real e controle de estoque máximo.
   * Suporte a venda avulsa ou vinculada a cliente cadastrado.
   * Modos de pagamento: Dinheiro, PIX, Cartão de Débito, Cartão de Crédito e Fiado.

2. **Clientes & Gestão de Fiado:**
   * Cadastro completo de clientes (Pessoa Física / Jurídica).
   * Controle automatizado de saldo devedor e contas a receber.
   * Segregação automática entre vendas liquidadas e vendas a prazo.

3. **Caixa da Loja:**
   * Controle de abertura e fechamento de caixa por operador.
   * Sangrias, suprimentos e histórico de movimentações da gaveta.

4. **Produtos & Estoque:**
   * Catálogo de produtos com precificação e código de barras.
   * Baixa automatizada na venda e incremento no recebimento de compras.

5. **Compras & Fornecedores:**
   * Gestão de pedidos de compra junto a fornecedores.
   * Action customizada no Admin para confirmação de entrega com atualização automática de estoque.

6. **Dashboard Geral de Métricas:**
   * Indicadores em tempo real: Vendas Hoje, Faturamento Real (Líquido), Contas a Receber (Fiado) e Clientes Ativos.
   * Cards interativos que levam a relatórios analíticos detalhados.
   * Gráfico de faturamento dos últimos 7 dias via Chart.js.

7. **Financeiro & DRE:**
   * DRE Demonstrativo de Resultados, contas a pagar e controle de comissões de vendedores.

8. **Frota, Expedição, Funcionários e GED (Documentos):**
   * Módulos complementares para logística interna, ordens de entrega, cargos/permissões e gestão de documentos.

---

## 🛠️ Guia de Instalação e Execução Local

### Pré-requisitos
* Python 3.10+
* Git

### Passo a Passo

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/lojas-JBS.git](https://github.com/seu-usuario/lojas-JBS.git)
   cd lojas-JBS