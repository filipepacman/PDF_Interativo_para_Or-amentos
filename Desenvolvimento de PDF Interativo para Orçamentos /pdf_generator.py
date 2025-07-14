from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

class EMPRESAPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Configurar estilos customizados para o PDF EMPRESA"""
        # Estilo para título principal
        self.styles.add(ParagraphStyle(
            name='EMPRESATitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1e40af'),
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        # Estilo para subtítulos
        self.styles.add(ParagraphStyle(
            name='EMPRESASubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            alignment=TA_LEFT,
            spaceAfter=10
        ))
        
        # Estilo para cabeçalho de disciplina
        self.styles.add(ParagraphStyle(
            name='DisciplinaHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.white,
            backColor=colors.HexColor('#1e40af'),
            alignment=TA_CENTER,
            spaceAfter=15,
            spaceBefore=15
        ))
        
        # Estilo para texto normal
        self.styles.add(ParagraphStyle(
            name='EMPRESANormal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#374151'),
            alignment=TA_LEFT
        ))
        
        # Estilo para valores monetários
        self.styles.add(ParagraphStyle(
            name='EMPRESAMoney',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#059669'),
            alignment=TA_RIGHT,
            fontName='Helvetica-Bold'
        ))

    def gerar_pdf_orcamento(self, orcamento_data, itens_data, output_path):
        """Gerar PDF do orçamento baseado no template EMPRESA"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=20*mm
        )
        
        story = []
        
        # Cabeçalho principal
        story.extend(self._criar_cabecalho(orcamento_data))
        
        # Informações do cliente e projeto
        story.extend(self._criar_info_cliente(orcamento_data))
        
        # Itens agrupados por disciplina
        story.extend(self._criar_itens_por_disciplina(itens_data))
        
        # Resumo geral
        story.extend(self._criar_resumo_geral(orcamento_data, itens_data))
        
        # Condições contratuais
        story.extend(self._criar_condicoes_contratuais(orcamento_data))
        
        # Observações e anexos
        story.extend(self._criar_observacoes_anexos(orcamento_data))
        
        # Gerar o PDF
        doc.build(story)
        return output_path

    def _criar_cabecalho(self, orcamento_data):
        """Criar cabeçalho do documento"""
        elements = []
        
        # Título EMPRESA
        elements.append(Paragraph("EMPRESA", self.styles['EMPRESATitle']))
        elements.append(Paragraph("ENGENHARIA E FACHADAS", self.styles['EMPRESASubtitle']))
        elements.append(Spacer(1, 20))
        
        # Título da proposta
        elements.append(Paragraph("P R O P O S T A", self.styles['EMPRESATitle']))
        elements.append(Spacer(1, 20))
        
        # Informações do orçamento
        info_data = [
            ['ORÇAMENTO:', orcamento_data.get('numero', 'N/A')],
            ['DATA:', datetime.now().strftime('%d/%m/%Y')],
            ['ALTURA DO PRÉDIO:', orcamento_data.get('altura_predio', 'N/A')],
            ['ESCALA DE BEAUFORT:', orcamento_data.get('escala_beaufort', 'N/A')]
        ]
        
        info_table = Table(info_data, colWidths=[40*mm, 60*mm])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db'))
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 20))
        
        return elements

    def _criar_info_cliente(self, orcamento_data):
        """Criar seção de informações do cliente"""
        elements = []
        
        # Projeto
        elements.append(Paragraph(f"<b>PROJETO:</b> {orcamento_data.get('projeto_nome', 'N/A')}", self.styles['EMPRESASubtitle']))
        
        # Endereço
        endereco = orcamento_data.get('cliente_endereco', 'N/A')
        elements.append(Paragraph(f"<b>ENDEREÇO:</b> {endereco}", self.styles['EMPRESANormal']))
        elements.append(Spacer(1, 10))
        
        # Cliente
        elements.append(Paragraph(f"<b>CLIENTE:</b> {orcamento_data.get('cliente_nome', 'N/A')}", self.styles['EMPRESASubtitle']))
        elements.append(Spacer(1, 20))
        
        return elements

    def _criar_itens_por_disciplina(self, itens_data):
        """Criar seções de itens agrupados por disciplina"""
        elements = []
        
        # Agrupar itens por disciplina
        disciplinas = {}
        for item in itens_data:
            disciplina = item.get('disciplina_nome', 'OUTROS')
            if disciplina not in disciplinas:
                disciplinas[disciplina] = []
            disciplinas[disciplina].append(item)
        
        # Criar seção para cada disciplina
        for disciplina_nome, itens in disciplinas.items():
            elements.append(PageBreak())
            
            # Cabeçalho da disciplina
            elements.append(Paragraph(f"DISCIPLINA: {disciplina_nome}", self.styles['DisciplinaHeader']))
            elements.append(Spacer(1, 15))
            
            # Tabela de itens
            item_counter = 1
            for item in itens:
                elements.extend(self._criar_item_detalhado(item, item_counter))
                item_counter += 1
            
            # Total da disciplina
            total_disciplina = sum(item.get('preco_total', 0) for item in itens)
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(
                f"<b>TOTAL {disciplina_nome}: {self._formatar_moeda(total_disciplina)}</b>",
                self.styles['EMPRESAMoney']
            ))
            elements.append(Spacer(1, 20))
        
        return elements

    def _criar_item_detalhado(self, item, numero):
        """Criar detalhes de um item específico"""
        elements = []
        
        # Número e código do item
        elements.append(Paragraph(f"<b>{numero:02d}</b>", self.styles['EMPRESASubtitle']))
        elements.append(Spacer(1, 5))
        
        # Título do item
        elements.append(Paragraph(f"<b>{item.get('titulo', 'N/A')}</b>", self.styles['EMPRESASubtitle']))
        
        # Descrição técnica
        descricao = item.get('descritivo_tecnico', 'N/A')
        elements.append(Paragraph(descricao, self.styles['EMPRESANormal']))
        elements.append(Spacer(1, 10))
        
        # Tabela com dados do item
        dados_item = [
            ['CÓDIGO', 'UM', 'QUANT', 'VALOR UNIT', 'TOTAL'],
            [
                item.get('codigo', 'N/A'),
                item.get('unidade_medida', 'N/A'),
                f"{item.get('quantidade', 0):.3f}",
                self._formatar_moeda(item.get('preco_unitario', 0)),
                self._formatar_moeda(item.get('preco_total', 0))
            ]
        ]
        
        item_table = Table(dados_item, colWidths=[25*mm, 15*mm, 20*mm, 30*mm, 30*mm])
        item_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db'))
        ]))
        
        elements.append(item_table)
        elements.append(Spacer(1, 15))
        
        return elements

    def _criar_resumo_geral(self, orcamento_data, itens_data):
        """Criar resumo geral do orçamento"""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("RESUMO GERAL", self.styles['DisciplinaHeader']))
        elements.append(Spacer(1, 20))
        
        # Agrupar totais por disciplina
        disciplinas_totais = {}
        for item in itens_data:
            disciplina = item.get('disciplina_nome', 'OUTROS')
            if disciplina not in disciplinas_totais:
                disciplinas_totais[disciplina] = 0
            disciplinas_totais[disciplina] += item.get('preco_total', 0)
        
        # Tabela de resumo
        resumo_data = [['DISCIPLINA', 'TOTAL']]
        for disciplina, total in disciplinas_totais.items():
            resumo_data.append([disciplina, self._formatar_moeda(total)])
        
        # Total geral
        total_geral = sum(disciplinas_totais.values())
        resumo_data.append(['TOTAL GERAL', self._formatar_moeda(total_geral)])
        
        resumo_table = Table(resumo_data, colWidths=[100*mm, 50*mm])
        resumo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db'))
        ]))
        
        elements.append(resumo_table)
        elements.append(Spacer(1, 30))
        
        return elements

    def _criar_condicoes_contratuais(self, orcamento_data):
        """Criar seção de condições contratuais"""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("CONDIÇÕES CONTRATUAIS", self.styles['DisciplinaHeader']))
        elements.append(Spacer(1, 20))
        
        # Condições padrão (simuladas - em produção viriam do banco)
        condicoes = """
CONTRATAÇÃO - Em regime de Empreitada Global.

PRAZOS DA OBRA - O prazo de execução da obra será de 60 dias corridos.

EXECUÇÃO DA OBRA - Será realizada com empresas instaladoras devidamente homologadas pela EMPRESA no prazo especificado de forma continua. Solicitações de interrupções de serviços, faseamento da execução ou qualquer outra solicitação do cliente de pausa ou atraso na execução serão orçadas à parte.

PAGAMENTO - Medições quinzenais com entregas de notas sempre nos dias 5 e 20 de cada mês e pagamentos das notas entregues nos dias 15 e 20, respectivamente.

FATURAMENTO - Emissão direta de notas fiscais de fornecedores e prestadores de serviços para evitar a bitributação, com o pagamento segundo a forma estabelecida.

IMPOSTOS - Inclusos (ISS, PIS, COFINS, CS, INSS). Na eventualidade da criação de um novo imposto, sua incidência no custo final será absorvida pelo cliente.

VALIDADE - A proposta de preços tem validade de 30 dias.

PROJETO e ART - Inclusos na proposta o projeto e o recolhimento da ART de Projeto e montagem, cujo valor é 10% sobre os itens de execução de trabalhos.

GARANTIA LIMITADA - de 5 anos a contar do término dos serviços conforme termo de garantia.

COMPATIBILIZAÇÃO DE PROJETOS - os valores podem ser reajustados em virtude da compatibilização do caderno técnico EMPRESA com os demais elementos construtivos.

TESTES E ENSAIOS - não incluído nenhum tipo de ensaio nem teste nesta proposta.

CANTEIRO DE OBRAS e CONTÂINERS - O cliente fornecerá espaço adequado às necessidades.

ENERGIA ELÉTRICA E ÁGUA - O cliente deverá fazer conexões a seus quadros existentes para pontos de energia elétrica para suprir a obra.

RETENÇÃO DE GARANTIA DE OBRA - se aplicará um 5% sobre os itens de execução de trabalhos, somente.

ANDAIMES - Balancin elétrico (locação, montagem e desmontagem) - por conta do cliente.
        """
        
        elements.append(Paragraph(condicoes, self.styles['EMPRESANormal']))
        elements.append(Spacer(1, 20))
        
        return elements

    def _criar_observacoes_anexos(self, orcamento_data):
        """Criar seção de observações e anexos"""
        elements = []
        
        # Observações
        observacoes = orcamento_data.get('observacoes', '')
        if observacoes:
            elements.append(Paragraph("OBSERVAÇÕES", self.styles['EMPRESASubtitle']))
            elements.append(Paragraph(observacoes, self.styles['EMPRESANormal']))
            elements.append(Spacer(1, 15))
        
        # Anexos
        anexos = orcamento_data.get('anexos', '')
        if anexos:
            elements.append(Paragraph("ANEXOS", self.styles['EMPRESASubtitle']))
            elements.append(Paragraph(anexos, self.styles['EMPRESANormal']))
            elements.append(Spacer(1, 15))
        
        # Rodapé com informações da empresa
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(
            "EMPRESA ENGENHARIA LTDA - CNPJ XX.XXX.XXX/0001-XX",
            self.styles['EMPRESANormal']
        ))
        elements.append(Paragraph(
            "Endereço da empresa - Telefone - Email",
            self.styles['EMPRESANormal']
        ))
        
        return elements

    def _formatar_moeda(self, valor):
        """Formatar valor como moeda brasileira"""
        return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Função utilitária para uso nas rotas
def gerar_pdf_orcamento(orcamento_data, itens_data, output_dir):
    """Função principal para gerar PDF de orçamento"""
    generator = EMPRESAPDFGenerator()
    
    # Nome do arquivo
    numero_orcamento = orcamento_data.get('numero', 'orcamento')
    filename = f"{numero_orcamento}.pdf"
    output_path = os.path.join(output_dir, filename)
    
    # Garantir que o diretório existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Gerar o PDF
    return generator.gerar_pdf_orcamento(orcamento_data, itens_data, output_path)

