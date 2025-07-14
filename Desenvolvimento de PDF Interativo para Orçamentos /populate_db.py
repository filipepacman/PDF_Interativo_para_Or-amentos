#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados iniciais do EMPRESA
Baseado no orçamento de exemplo fornecido
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from src.models.orcamento import db, Disciplina, Item, CondicaoContratual

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def populate_database():
    app = create_app()
    
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Limpar dados existentes (cuidado em produção!)
        db.session.query(Item).delete()
        db.session.query(Disciplina).delete()
        db.session.query(CondicaoContratual).delete()
        
        # Criar disciplinas
        disciplinas_data = [
            {
                'nome': 'FACHADA VENTILADA',
                'descricao': 'Sistemas de fachada ventilada com diferentes tecnologias'
            },
            {
                'nome': 'BRISE SOLEIL',
                'descricao': 'Sistemas de proteção solar e brise'
            },
            {
                'nome': 'IMPERMEABILIZAÇÃO',
                'descricao': 'Serviços de impermeabilização diversos'
            },
            {
                'nome': 'MEIOS AUXILIARES',
                'descricao': 'Equipamentos e ferramentas necessárias para execução'
            }
        ]
        
        disciplinas = {}
        for disc_data in disciplinas_data:
            disciplina = Disciplina(**disc_data)
            db.session.add(disciplina)
            db.session.flush()  # Para obter o ID
            disciplinas[disc_data['nome']] = disciplina
        
        # Criar itens baseados no orçamento de exemplo
        itens_data = [
            # FACHADA VENTILADA
            {
                'codigo': '4555',
                'titulo': 'VTACK SYSTEM',
                'descritivo_tecnico': 'Acabamento de peitoril para fechamento da fachada ventilada com porcelanato. Obs. Não inclui o fornecimento do revestimento.',
                'unidade_medida': 'm²',
                'preco_unitario_padrao': 1200.00,
                'disciplina_id': disciplinas['FACHADA VENTILADA'].id
            },
            {
                'codigo': '36745',
                'titulo': 'VLASTRA SYSTEM',
                'descritivo_tecnico': 'Sistema de fachada ventilada com tecnologia avançada para revestimentos diversos.',
                'unidade_medida': 'm²',
                'preco_unitario_padrao': 95.40,
                'disciplina_id': disciplinas['FACHADA VENTILADA'].id
            },
            {
                'codigo': '51258',
                'titulo': 'VHOOK SYSTEM',
                'descritivo_tecnico': 'Sistema de Fachada Ventilada, fornecendo os materiais necessários, formado por perfil horizontal de Alumínio, fixado com parafusos de bucha 100x80mm, incluindo ganchos colados na parte dorsal do revestimento, separadores de PVC para juntas e Polímero MS para colagem. Incluindo montagem realizada por empresa especializada. Obs. Não inclui o fornecimento do revestimento',
                'unidade_medida': 'm²',
                'preco_unitario_padrao': 102.40,
                'disciplina_id': disciplinas['FACHADA VENTILADA'].id
            },
            {
                'codigo': '48883',
                'titulo': 'VSLOT SYSTEM',
                'descritivo_tecnico': 'Impermeabilização em telhas de fibrocimento com membrana líquida elastômera da marca EMPRESA Vlaje fabricado por ISOLASTECH. Se aplicará uma demão de PRIMER reforçada com tela no perímetro da telha e logo receberá uma segunda demão do FINALIZADOR com proteção a raios UV.',
                'unidade_medida': 'm²',
                'preco_unitario_padrao': 372.60,
                'disciplina_id': disciplinas['FACHADA VENTILADA'].id
            },
            {
                'codigo': '98772',
                'titulo': 'VCOTA SYSTEM',
                'descritivo_tecnico': 'Sistema de coroamento e acabamento para fachadas ventiladas com materiais de alta qualidade.',
                'unidade_medida': 'm²',
                'preco_unitario_padrao': 4600.00,
                'disciplina_id': disciplinas['FACHADA VENTILADA'].id
            },
            {
                'codigo': '4575',
                'titulo': 'VHOOK SYSTEM - Perfil Alumínio',
                'descritivo_tecnico': 'Perfil de alumínio pintado de cor a definir, clipado a suportes. Para fechamento inferior da fachada ventilada. Projeto executivo, gerenciamento e fornecimento de materiais.',
                'unidade_medida': 'm²',
                'preco_unitario_padrao': 35.22,
                'disciplina_id': disciplinas['FACHADA VENTILADA'].id
            },
            {
                'codigo': '36225',
                'titulo': 'VTACK SYSTEM - Primer',
                'descritivo_tecnico': 'Se aplicará uma demão de PRIMER reforçada com tela no perímetro da telha e logo receberá uma segunda demão do FINALIZADOR com proteção a raios UV. **Esta incluso mão de obra e materiais.',
                'unidade_medida': 'm²',
                'preco_unitario_padrao': 45.90,
                'disciplina_id': disciplinas['FACHADA VENTILADA'].id
            },
            {
                'codigo': '54458',
                'titulo': 'VSLOT SYSTEM - Clipados',
                'descritivo_tecnico': 'Clipados sobre suporte especial instalado no tubular vertical, que a sua vez estes estarão fixados com mensulas a parede portante. O coroamento e fechamento inferior será por um perfil tubular de 4x2 polegadas. Toda a estrutura será com material de alumínio com tratamento de anodizado natural. **Inclui mão de obra e materiais.',
                'unidade_medida': 'm²',
                'preco_unitario_padrao': 85.00,
                'disciplina_id': disciplinas['FACHADA VENTILADA'].id
            },
            {
                'codigo': '48943',
                'titulo': 'CLAW SUPPORT',
                'descritivo_tecnico': 'Brise com perfis tubulares, cliptados sobre suporte especial instalado no tubular vertical, que a sua vez estes estarão fixados com mensulas a parede portante. O coroamento e fechamento inferior será por um perfil tubular de 4x2 polegadas. Toda a estrutura será com material de alumínio com tratamento de anodizado natural. O coroamento e fechamento inferior será por um perfil tubular de 4x2 polegadas. **Inclui mão de obra e materiais.',
                'unidade_medida': 'm²',
                'preco_unitario_padrao': 1715.69,
                'disciplina_id': disciplinas['FACHADA VENTILADA'].id
            },
            {
                'codigo': '97532',
                'titulo': 'Seguro de Responsabilidade Civil',
                'descritivo_tecnico': 'Seguro de responsabilidade civil para cobertura durante a execução dos serviços.',
                'unidade_medida': 'VB',
                'preco_unitario_padrao': 161057.13,
                'disciplina_id': disciplinas['FACHADA VENTILADA'].id
            },
            
            # BRISE SOLEIL
            {
                'codigo': '8599',
                'titulo': 'BRISE - Sistema Básico',
                'descritivo_tecnico': 'Sistema de brise soleil com perfis de alumínio para proteção solar.',
                'unidade_medida': 'm',
                'preco_unitario_padrao': 1200.00,
                'disciplina_id': disciplinas['BRISE SOLEIL'].id
            },
            {
                'codigo': '8756',
                'titulo': 'BRISE - Sistema Avançado',
                'descritivo_tecnico': 'Sistema avançado de brise soleil com controle automatizado e materiais de alta performance.',
                'unidade_medida': 'm',
                'preco_unitario_padrao': 95.40,
                'disciplina_id': disciplinas['BRISE SOLEIL'].id
            },
            {
                'codigo': '8327',
                'titulo': 'BRISE - Perfis Especiais',
                'descritivo_tecnico': 'Sistema de Fachada Ventilada, fornecendo os materiais necessários, formado por perfil horizontal de Alumínio, fixado com parafusos de bucha 100x80mm, incluindo ganchos colados na parte dorsal do revestimento, separadores de PVC para juntas e Polímero MS para colagem. Incluindo montagem realizada por empresa especializada. Obs. Não inclui o fornecimento do revestimento',
                'unidade_medida': 'm',
                'preco_unitario_padrao': 102.40,
                'disciplina_id': disciplinas['BRISE SOLEIL'].id
            },
            {
                'codigo': '8965',
                'titulo': 'BRISE - Acabamento',
                'descritivo_tecnico': 'Acabamentos e detalhes finais para sistemas de brise soleil.',
                'unidade_medida': 'm',
                'preco_unitario_padrao': 372.60,
                'disciplina_id': disciplinas['BRISE SOLEIL'].id
            },
            
            # IMPERMEABILIZAÇÃO
            {
                'codigo': '4555-IMP',
                'titulo': 'VTELHA',
                'descritivo_tecnico': 'Sistema de impermeabilização para telhas com materiais de alta qualidade.',
                'unidade_medida': 'un',
                'preco_unitario_padrao': 55.00,
                'disciplina_id': disciplinas['IMPERMEABILIZAÇÃO'].id
            },
            {
                'codigo': '36745-IMP',
                'titulo': 'VFLEX SACADAS',
                'descritivo_tecnico': 'Acabamento de peitoril para fechamento da fachada ventilada com porcelanato. Obs. Não inclui o fornecimento do revestimento.',
                'unidade_medida': 'un',
                'preco_unitario_padrao': 50.00,
                'disciplina_id': disciplinas['IMPERMEABILIZAÇÃO'].id
            }
        ]
        
        # Adicionar equipamentos/meios auxiliares
        equipamentos_data = [
            {
                'codigo': '7523',
                'titulo': 'Locação de Plataforma Elevatória articulada',
                'descritivo_tecnico': 'Locação mensal de plataforma elevatória articulada para trabalhos em altura.',
                'unidade_medida': 'MÊS',
                'preco_unitario_padrao': 133.00,
                'disciplina_id': disciplinas['MEIOS AUXILIARES'].id
            },
            {
                'codigo': '7566',
                'titulo': 'Locação de Plataforma Tesoura 15,0 m',
                'descritivo_tecnico': 'Locação mensal de plataforma tesoura com altura de 15 metros.',
                'unidade_medida': 'MÊS',
                'preco_unitario_padrao': 53.00,
                'disciplina_id': disciplinas['MEIOS AUXILIARES'].id
            },
            {
                'codigo': '7955',
                'titulo': 'Locação de Plataforma Tesoura 13,8 m',
                'descritivo_tecnico': 'Locação mensal de plataforma tesoura com altura de 13,8 metros.',
                'unidade_medida': 'MÊS',
                'preco_unitario_padrao': 1230.00,
                'disciplina_id': disciplinas['MEIOS AUXILIARES'].id
            },
            {
                'codigo': '7441',
                'titulo': 'Locação de Plataforma Elevatória articulada 20,15',
                'descritivo_tecnico': 'Locação mensal de plataforma elevatória articulada com altura de 20,15 metros.',
                'unidade_medida': 'MÊS',
                'preco_unitario_padrao': 1600.00,
                'disciplina_id': disciplinas['MEIOS AUXILIARES'].id
            },
            {
                'codigo': '7456',
                'titulo': 'Ferramentas e Materiais diversos',
                'descritivo_tecnico': 'Conjunto de ferramentas e materiais diversos necessários para execução.',
                'unidade_medida': 'VB',
                'preco_unitario_padrao': 300.00,
                'disciplina_id': disciplinas['MEIOS AUXILIARES'].id
            },
            {
                'codigo': '7854',
                'titulo': 'Disco de corte',
                'descritivo_tecnico': 'Discos de corte para equipamentos diversos.',
                'unidade_medida': 'MÊS',
                'preco_unitario_padrao': 1260.00,
                'disciplina_id': disciplinas['MEIOS AUXILIARES'].id
            }
        ]
        
        # Adicionar todos os itens
        all_items = itens_data + equipamentos_data
        for item_data in all_items:
            item = Item(**item_data)
            db.session.add(item)
        
        # Criar condições contratuais
        condicoes_data = [
            {
                'nome': 'Modelo Obras Pequenas',
                'descricao': 'Condições contratuais padrão para obras de pequeno porte',
                'conteudo': '''CONTRATAÇÃO - Em regime de Empreitada Global.
PRAZOS DA OBRA - O prazo de execução da obra será de 30 dias corridos.
EXECUÇÃO DA OBRA - Será realizada com empresas instaladoras devidamente homologadas pela EMPRESA no prazo especificado de forma continua.
PAGAMENTO - Medições quinzenais com entregas de notas sempre nos dias 5 e 20 de cada mês.
FATURAMENTO - Emissão direta de notas fiscais de fornecedores e prestadores de serviços.
IMPOSTOS - Inclusos (ISS, PIS, COFINS, CS, INSS).
VALIDADE - A proposta de preços tem validade de 30 dias.
GARANTIA LIMITADA - de 2 anos a contar do término dos serviços.'''
            },
            {
                'nome': 'Modelo Obras Grandes',
                'descricao': 'Condições contratuais padrão para obras de grande porte',
                'conteudo': '''CONTRATAÇÃO - Em regime de Empreitada Global.
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
ANDAIMES - Balancin elétrico (locação, montagem e desmontagem) - por conta do cliente.'''
            },
            {
                'nome': 'Modelo Internacional',
                'descricao': 'Condições contratuais para projetos internacionais',
                'conteudo': '''CONTRACT - Global Contract basis.
PROJECT TIMELINE - The execution period will be 90 calendar days.
PROJECT EXECUTION - Will be carried out by certified installation companies approved by EMPRESA within the specified timeframe.
PAYMENT - Biweekly measurements with invoice delivery on the 5th and 20th of each month.
BILLING - Direct invoice issuance from suppliers and service providers.
TAXES - Included (local taxes and fees as applicable).
VALIDITY - Price proposal valid for 45 days.
LIMITED WARRANTY - 5 years from service completion date.
CURRENCY - All values in USD unless otherwise specified.
INTERNATIONAL SHIPPING - Included for materials and equipment.
COMPLIANCE - All work will comply with local building codes and international standards.'''
            }
        ]
        
        for cond_data in condicoes_data:
            condicao = CondicaoContratual(**cond_data)
            db.session.add(condicao)
        
        # Salvar todas as alterações
        db.session.commit()
        print("Banco de dados populado com sucesso!")
        print(f"Disciplinas criadas: {len(disciplinas_data)}")
        print(f"Itens criados: {len(all_items)}")
        print(f"Condições contratuais criadas: {len(condicoes_data)}")

if __name__ == '__main__':
    populate_database()

