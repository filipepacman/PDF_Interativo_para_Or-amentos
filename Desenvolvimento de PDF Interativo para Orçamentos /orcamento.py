from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com itens
    itens = db.relationship('Item', backref='disciplina', lazy=True)
    
    def __repr__(self):
        return f'<Disciplina {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'ativo': self.ativo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descritivo_tecnico = db.Column(db.Text, nullable=False)
    unidade_medida = db.Column(db.String(10), nullable=False)  # m², ml, unid, kg, etc.
    preco_unitario_padrao = db.Column(db.Numeric(10, 2), nullable=False)
    link_detalhe_tecnico = db.Column(db.String(500))
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Chave estrangeira para disciplina
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=False)
    
    def __repr__(self):
        return f'<Item {self.codigo} - {self.titulo}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'titulo': self.titulo,
            'descritivo_tecnico': self.descritivo_tecnico,
            'unidade_medida': self.unidade_medida,
            'preco_unitario_padrao': float(self.preco_unitario_padrao),
            'link_detalhe_tecnico': self.link_detalhe_tecnico,
            'ativo': self.ativo,
            'disciplina_id': self.disciplina_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CondicaoContratual(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)  # Ex: "Modelo Obras Pequenas"
    descricao = db.Column(db.Text)
    conteudo = db.Column(db.Text, nullable=False)  # Conteúdo das condições
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CondicaoContratual {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'conteudo': self.conteudo,
            'ativo': self.ativo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Orcamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    cliente_nome = db.Column(db.String(200), nullable=False)
    cliente_endereco = db.Column(db.Text)
    projeto_nome = db.Column(db.String(200), nullable=False)
    altura_predio = db.Column(db.String(20))
    escala_beaufort = db.Column(db.String(20))
    observacoes = db.Column(db.Text)
    anexos = db.Column(db.Text)  # Lista de anexos separados por vírgula
    total_geral = db.Column(db.Numeric(12, 2), default=0)
    condicao_contratual_id = db.Column(db.Integer, db.ForeignKey('condicao_contratual.id'))
    clausulas_adicionais = db.Column(db.Text)  # Cláusulas personalizadas
    status = db.Column(db.String(20), default='rascunho')  # rascunho, finalizado, enviado
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    condicao_contratual = db.relationship('CondicaoContratual', backref='orcamentos')
    itens_orcamento = db.relationship('ItemOrcamento', backref='orcamento', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Orcamento {self.numero}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'cliente_nome': self.cliente_nome,
            'cliente_endereco': self.cliente_endereco,
            'projeto_nome': self.projeto_nome,
            'altura_predio': self.altura_predio,
            'escala_beaufort': self.escala_beaufort,
            'observacoes': self.observacoes,
            'anexos': self.anexos,
            'total_geral': float(self.total_geral) if self.total_geral else 0,
            'condicao_contratual_id': self.condicao_contratual_id,
            'clausulas_adicionais': self.clausulas_adicionais,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ItemOrcamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orcamento_id = db.Column(db.Integer, db.ForeignKey('orcamento.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=True)  # Pode ser None para itens personalizados
    
    # Dados do item (copiados ou personalizados)
    codigo = db.Column(db.String(20), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descritivo_tecnico = db.Column(db.Text, nullable=False)
    unidade_medida = db.Column(db.String(10), nullable=False)
    quantidade = db.Column(db.Numeric(10, 3), nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    preco_total = db.Column(db.Numeric(12, 2), nullable=False)
    link_detalhe_tecnico = db.Column(db.String(500))
    disciplina_nome = db.Column(db.String(100), nullable=False)
    ordem = db.Column(db.Integer, default=0)  # Para ordenação dentro da disciplina
    
    # Relacionamento
    item = db.relationship('Item', backref='itens_orcamento')
    
    def __repr__(self):
        return f'<ItemOrcamento {self.codigo} - Qtd: {self.quantidade}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'orcamento_id': self.orcamento_id,
            'item_id': self.item_id,
            'codigo': self.codigo,
            'titulo': self.titulo,
            'descritivo_tecnico': self.descritivo_tecnico,
            'unidade_medida': self.unidade_medida,
            'quantidade': float(self.quantidade),
            'preco_unitario': float(self.preco_unitario),
            'preco_total': float(self.preco_total),
            'link_detalhe_tecnico': self.link_detalhe_tecnico,
            'disciplina_nome': self.disciplina_nome,
            'ordem': self.ordem
        }

