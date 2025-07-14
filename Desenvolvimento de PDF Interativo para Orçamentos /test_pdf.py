#!/usr/bin/env python3
"""
Script para testar a geração de PDF
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.pdf_generator import gerar_pdf_orcamento

def testar_geracao_pdf():
    """Testar a geração de PDF com dados de exemplo"""
    
    # Dados de exemplo do orçamento
    orcamento_data = {
        'numero': 'ORC-TEST-001',
        'cliente_nome': 'MARCELO PEREZ LTDA',
        'cliente_endereco': 'RUA FRANCISCO OTAVIANO, N° 59 ARPOADOR\nRIO DE JANEIRO - RJ',
        'projeto_nome': 'CYRELA - ON THE SEA ARPOADOR',
        'altura_predio': '50M',
        'escala_beaufort': '01',
        'observacoes': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.',
        'anexos': 'PROJETOS QUANTITATIVOS SUPERFÍCIES\nRENDER DETALHE E ACABAMENTO',
        'total_geral': 3723120.73
    }
    
    # Dados de exemplo dos itens
    itens_data = [
        {
            'id': 1,
            'codigo': '4555',
            'titulo': 'VTACK SYSTEM',
            'descritivo_tecnico': 'Acabamento de peitoril para fechamento da fachada ventilada com porcelanato. Obs. Não inclui o fornecimento do revestimento.',
            'unidade_medida': 'm²',
            'quantidade': 1.0,
            'preco_unitario': 1200.00,
            'preco_total': 1200.00,
            'disciplina_nome': 'FACHADA VENTILADA'
        },
        {
            'id': 2,
            'codigo': '36745',
            'titulo': 'VLASTRA SYSTEM',
            'descritivo_tecnico': 'Sistema de fachada ventilada com tecnologia avançada para revestimentos diversos.',
            'unidade_medida': 'm²',
            'quantidade': 1683.0,
            'preco_unitario': 95.40,
            'preco_total': 160558.20,
            'disciplina_nome': 'FACHADA VENTILADA'
        },
        {
            'id': 3,
            'codigo': '51258',
            'titulo': 'VHOOK SYSTEM',
            'descritivo_tecnico': 'Sistema de Fachada Ventilada, fornecendo os materiais necessários, formado por perfil horizontal de Alumínio, fixado com parafusos de bucha 100x80mm, incluindo ganchos colados na parte dorsal do revestimento, separadores de PVC para juntas e Polímero MS para colagem. Incluindo montagem realizada por empresa especializada. Obs. Não inclui o fornecimento do revestimento',
            'unidade_medida': 'm²',
            'quantidade': 5190.30,
            'preco_unitario': 102.40,
            'preco_total': 531486.72,
            'disciplina_nome': 'FACHADA VENTILADA'
        },
        {
            'id': 4,
            'codigo': '8599',
            'titulo': 'BRISE - Sistema Básico',
            'descritivo_tecnico': 'Sistema de brise soleil com perfis de alumínio para proteção solar.',
            'unidade_medida': 'm',
            'quantidade': 200.0,
            'preco_unitario': 1200.00,
            'preco_total': 240000.00,
            'disciplina_nome': 'BRISE SOLEIL'
        },
        {
            'id': 5,
            'codigo': '7523',
            'titulo': 'Locação de Plataforma Elevatória articulada',
            'descritivo_tecnico': 'Locação mensal de plataforma elevatória articulada para trabalhos em altura.',
            'unidade_medida': 'MÊS',
            'quantidade': 3.0,
            'preco_unitario': 133.00,
            'preco_total': 399.00,
            'disciplina_nome': 'MEIOS AUXILIARES'
        }
    ]
    
    # Diretório de saída
    output_dir = '/home/ubuntu/orcamento-EMPRESA/pdfs'
    
    try:
        # Gerar PDF
        pdf_path = gerar_pdf_orcamento(orcamento_data, itens_data, output_dir)
        print(f"PDF gerado com sucesso: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return None

if __name__ == '__main__':
    testar_geracao_pdf()

