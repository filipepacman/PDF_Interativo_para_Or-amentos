import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button.jsx";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card.jsx";
import { Input } from "@/components/ui/input.jsx";
import { Label } from "@/components/ui/label.jsx";
import { Textarea } from "@/components/ui/textarea.jsx";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select.jsx";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table.jsx";
import { Badge } from "@/components/ui/badge.jsx";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs.jsx";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog.jsx";
import {
  Plus,
  Edit,
  Trash2,
  FileText,
  Calculator,
  Building2,
  Settings,
  Download,
} from "lucide-react";
import "./App.css";

// Configuração da API
const API_BASE_URL = window.location.origin + "/api";

function App() {
  const [disciplinas, setDisciplinas] = useState([]);
  const [itens, setItens] = useState([]);
  const [condicoes, setCondicoes] = useState([]);
  const [orcamentos, setOrcamentos] = useState([]);
  const [orcamentoAtual, setOrcamentoAtual] = useState(null);
  const [itensOrcamento, setItensOrcamento] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("orcamentos");
  const [dialogOpen, setDialogOpen] = useState(false);

  // Estados para formulários
  const [novoOrcamento, setNovoOrcamento] = useState({
    numero: "",
    cliente_nome: "",
    cliente_endereco: "",
    projeto_nome: "",
    altura_predio: "",
    escala_beaufort: "",
    observacoes: "",
    condicao_contratual_id: "",
    clausulas_adicionais: "",
  });

  const [novoItem, setNovoItem] = useState({
    item_id: "",
    quantidade: "",
    preco_unitario: "",
    disciplina_nome: "",
  });

  // Carregar dados iniciais
  useEffect(() => {
    carregarDados();
  }, []);

  const carregarDados = async () => {
    setLoading(true);
    try {
      // Carregar disciplinas
      const disciplinasRes = await fetch(`${API_BASE_URL}/disciplinas`);
      const disciplinasData = await disciplinasRes.json();
      setDisciplinas(disciplinasData);

      // Carregar itens
      const itensRes = await fetch(`${API_BASE_URL}/itens`);
      const itensData = await itensRes.json();
      setItens(itensData);

      // Carregar condições contratuais
      const condicoesRes = await fetch(`${API_BASE_URL}/condicoes-contratuais`);
      const condicoesData = await condicoesRes.json();
      setCondicoes(condicoesData);

      // Carregar orçamentos
      const orcamentosRes = await fetch(`${API_BASE_URL}/orcamentos`);
      const orcamentosData = await orcamentosRes.json();
      setOrcamentos(orcamentosData);
    } catch (error) {
      console.error("Erro ao carregar dados:", error);
      alert("Erro ao carregar dados. Verifique se o servidor está rodando.");
    } finally {
      setLoading(false);
    }
  };

  const criarOrcamento = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/orcamentos`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(novoOrcamento),
      });

      if (response.ok) {
        const novoOrc = await response.json();
        setOrcamentos([novoOrc, ...orcamentos]);
        setOrcamentoAtual(novoOrc);
        setItensOrcamento([]);
        setActiveTab("editor");
        setDialogOpen(false);

        // Limpar formulário
        setNovoOrcamento({
          numero: "",
          cliente_nome: "",
          cliente_endereco: "",
          projeto_nome: "",
          altura_predio: "",
          escala_beaufort: "",
          observacoes: "",
          condicao_contratual_id: "",
          clausulas_adicionais: "",
        });
      } else {
        alert("Erro ao criar orçamento");
      }
    } catch (error) {
      console.error("Erro ao criar orçamento:", error);
      alert("Erro ao criar orçamento");
    }
  };

  const carregarItensOrcamento = async (orcamentoId) => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/orcamentos/${orcamentoId}/itens`
      );
      if (response.ok) {
        const itensData = await response.json();
        setItensOrcamento(itensData);
      }
    } catch (error) {
      console.error("Erro ao carregar itens do orçamento:", error);
    }
  };

  const adicionarItem = async () => {
    if (!novoItem.item_id || !novoItem.quantidade || !orcamentoAtual) return;

    try {
      const response = await fetch(
        `${API_BASE_URL}/orcamentos/${orcamentoAtual.id}/itens`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            item_id: parseInt(novoItem.item_id),
            quantidade: parseFloat(novoItem.quantidade),
            preco_unitario: novoItem.preco_unitario
              ? parseFloat(novoItem.preco_unitario)
              : undefined,
          }),
        }
      );

      if (response.ok) {
        const novoItemOrcamento = await response.json();
        setItensOrcamento([...itensOrcamento, novoItemOrcamento]);

        // Recalcular total
        await recalcularTotal();

        // Limpar formulário
        setNovoItem({
          item_id: "",
          quantidade: "",
          preco_unitario: "",
          disciplina_nome: "",
        });
      } else {
        alert("Erro ao adicionar item");
      }
    } catch (error) {
      console.error("Erro ao adicionar item:", error);
      alert("Erro ao adicionar item");
    }
  };

  const removerItem = async (itemId) => {
    if (!orcamentoAtual) return;

    try {
      const response = await fetch(
        `${API_BASE_URL}/orcamentos/${orcamentoAtual.id}/itens/${itemId}`,
        {
          method: "DELETE",
        }
      );

      if (response.ok) {
        setItensOrcamento(itensOrcamento.filter((item) => item.id !== itemId));
        await recalcularTotal();
      } else {
        alert("Erro ao remover item");
      }
    } catch (error) {
      console.error("Erro ao remover item:", error);
      alert("Erro ao remover item");
    }
  };

  const recalcularTotal = async () => {
    if (!orcamentoAtual) return;

    try {
      const response = await fetch(
        `${API_BASE_URL}/orcamentos/${orcamentoAtual.id}/calcular-total`,
        {
          method: "POST",
        }
      );

      if (response.ok) {
        const data = await response.json();
        setOrcamentoAtual({ ...orcamentoAtual, total_geral: data.total_geral });

        // Atualizar na lista de orçamentos
        setOrcamentos(
          orcamentos.map((orc) =>
            orc.id === orcamentoAtual.id
              ? { ...orc, total_geral: data.total_geral }
              : orc
          )
        );
      }
    } catch (error) {
      console.error("Erro ao recalcular total:", error);
    }
  };

  const gerarPDF = async () => {
    if (!orcamentoAtual) return;

    try {
      const response = await fetch(
        `${API_BASE_URL}/orcamentos/${orcamentoAtual.id}/pdf`
      );

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;
        a.download = `${orcamentoAtual.numero}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        alert("Erro ao gerar PDF");
      }
    } catch (error) {
      console.error("Erro ao gerar PDF:", error);
      alert("Erro ao gerar PDF");
    }
  };

  const editarOrcamento = async (orcamento) => {
    setOrcamentoAtual(orcamento);
    await carregarItensOrcamento(orcamento.id);
    setActiveTab("editor");
  };

  const formatarMoeda = (valor) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(valor);
  };

  const formatarData = (dataString) => {
    return new Date(dataString).toLocaleDateString("pt-BR");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Carregando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <Building2 className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">EMPRESA</h1>
                <p className="text-sm text-gray-600">Sistema de Orçamentos</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-sm">
                v1.0.0
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs
          value={activeTab}
          onValueChange={setActiveTab}
          className="space-y-6"
        >
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger
              value="orcamentos"
              className="flex items-center space-x-2"
            >
              <FileText className="h-4 w-4" />
              <span>Orçamentos</span>
            </TabsTrigger>
            <TabsTrigger value="editor" className="flex items-center space-x-2">
              <Calculator className="h-4 w-4" />
              <span>Editor</span>
            </TabsTrigger>
            <TabsTrigger
              value="catalogo"
              className="flex items-center space-x-2"
            >
              <Building2 className="h-4 w-4" />
              <span>Catálogo</span>
            </TabsTrigger>
            <TabsTrigger
              value="configuracoes"
              className="flex items-center space-x-2"
            >
              <Settings className="h-4 w-4" />
              <span>Configurações</span>
            </TabsTrigger>
          </TabsList>

          {/* Aba Orçamentos */}
          <TabsContent value="orcamentos" className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-3xl font-bold text-gray-900">Orçamentos</h2>
              <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
                <DialogTrigger asChild>
                  <Button className="flex items-center space-x-2">
                    <Plus className="h-4 w-4" />
                    <span>Novo Orçamento</span>
                  </Button>
                </DialogTrigger>
                <DialogContent className="sm:max-w-[600px]">
                  <DialogHeader>
                    <DialogTitle>Criar Novo Orçamento</DialogTitle>
                    <DialogDescription>
                      Preencha as informações básicas do orçamento
                    </DialogDescription>
                  </DialogHeader>
                  <div className="grid gap-4 py-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="cliente_nome">Cliente</Label>
                        <Input
                          id="cliente_nome"
                          value={novoOrcamento.cliente_nome}
                          onChange={(e) =>
                            setNovoOrcamento({
                              ...novoOrcamento,
                              cliente_nome: e.target.value,
                            })
                          }
                          placeholder="Nome do cliente"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="projeto_nome">Projeto</Label>
                        <Input
                          id="projeto_nome"
                          value={novoOrcamento.projeto_nome}
                          onChange={(e) =>
                            setNovoOrcamento({
                              ...novoOrcamento,
                              projeto_nome: e.target.value,
                            })
                          }
                          placeholder="Nome do projeto"
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="cliente_endereco">Endereço</Label>
                      <Textarea
                        id="cliente_endereco"
                        value={novoOrcamento.cliente_endereco}
                        onChange={(e) =>
                          setNovoOrcamento({
                            ...novoOrcamento,
                            cliente_endereco: e.target.value,
                          })
                        }
                        placeholder="Endereço completo do projeto"
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="altura_predio">Altura do Prédio</Label>
                        <Input
                          id="altura_predio"
                          value={novoOrcamento.altura_predio}
                          onChange={(e) =>
                            setNovoOrcamento({
                              ...novoOrcamento,
                              altura_predio: e.target.value,
                            })
                          }
                          placeholder="Ex: 50M"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="escala_beaufort">
                          Escala de Beaufort
                        </Label>
                        <Input
                          id="escala_beaufort"
                          value={novoOrcamento.escala_beaufort}
                          onChange={(e) =>
                            setNovoOrcamento({
                              ...novoOrcamento,
                              escala_beaufort: e.target.value,
                            })
                          }
                          placeholder="Ex: 01"
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="condicao_contratual_id">
                        Condições Contratuais
                      </Label>
                      <Select
                        value={novoOrcamento.condicao_contratual_id}
                        onValueChange={(value) =>
                          setNovoOrcamento({
                            ...novoOrcamento,
                            condicao_contratual_id: value,
                          })
                        }
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Selecione as condições" />
                        </SelectTrigger>
                        <SelectContent>
                          {condicoes.map((condicao) => (
                            <SelectItem
                              key={condicao.id}
                              value={condicao.id.toString()}
                            >
                              {condicao.nome}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="observacoes">Observações</Label>
                      <Textarea
                        id="observacoes"
                        value={novoOrcamento.observacoes}
                        onChange={(e) =>
                          setNovoOrcamento({
                            ...novoOrcamento,
                            observacoes: e.target.value,
                          })
                        }
                        placeholder="Observações adicionais"
                      />
                    </div>
                  </div>
                  <div className="flex justify-end space-x-2">
                    <Button
                      variant="outline"
                      onClick={() => setDialogOpen(false)}
                    >
                      Cancelar
                    </Button>
                    <Button onClick={criarOrcamento}>Criar Orçamento</Button>
                  </div>
                </DialogContent>
              </Dialog>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Lista de Orçamentos</CardTitle>
                <CardDescription>
                  Gerencie todos os seus orçamentos
                </CardDescription>
              </CardHeader>
              <CardContent>
                {orcamentos.length === 0 ? (
                  <div className="text-center py-8">
                    <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600">
                      Nenhum orçamento criado ainda
                    </p>
                    <p className="text-sm text-gray-500">
                      Clique em "Novo Orçamento" para começar
                    </p>
                  </div>
                ) : (
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Número</TableHead>
                        <TableHead>Cliente</TableHead>
                        <TableHead>Projeto</TableHead>
                        <TableHead>Total</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Data</TableHead>
                        <TableHead>Ações</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {orcamentos.map((orcamento) => (
                        <TableRow key={orcamento.id}>
                          <TableCell className="font-medium">
                            {orcamento.numero}
                          </TableCell>
                          <TableCell>{orcamento.cliente_nome}</TableCell>
                          <TableCell>{orcamento.projeto_nome}</TableCell>
                          <TableCell>
                            {formatarMoeda(orcamento.total_geral)}
                          </TableCell>
                          <TableCell>
                            <Badge
                              variant={
                                orcamento.status === "finalizado"
                                  ? "default"
                                  : "secondary"
                              }
                            >
                              {orcamento.status}
                            </Badge>
                          </TableCell>
                          <TableCell>
                            {formatarData(orcamento.created_at)}
                          </TableCell>
                          <TableCell>
                            <div className="flex space-x-2">
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => editarOrcamento(orcamento)}
                              >
                                <Edit className="h-4 w-4" />
                              </Button>
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => {
                                  setOrcamentoAtual(orcamento);
                                  gerarPDF();
                                }}
                              >
                                <Download className="h-4 w-4" />
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Aba Editor */}
          <TabsContent value="editor" className="space-y-6">
            {!orcamentoAtual ? (
              <Card>
                <CardContent className="pt-6">
                  <div className="text-center py-8">
                    <Calculator className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600">
                      Selecione um orçamento para editar
                    </p>
                    <p className="text-sm text-gray-500">
                      Ou crie um novo orçamento na aba anterior
                    </p>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <>
                <div className="flex justify-between items-center">
                  <div>
                    <h2 className="text-3xl font-bold text-gray-900">
                      Editor de Orçamento
                    </h2>
                    <p className="text-gray-600">
                      {orcamentoAtual.numero} - {orcamentoAtual.cliente_nome}
                    </p>
                  </div>
                  <div className="flex space-x-2">
                    <Button
                      onClick={gerarPDF}
                      className="flex items-center space-x-2"
                    >
                      <Download className="h-4 w-4" />
                      <span>Gerar PDF</span>
                    </Button>
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Adicionar Item */}
                  <Card>
                    <CardHeader>
                      <CardTitle>Adicionar Item</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="item_select">Item</Label>
                        <Select
                          value={novoItem.item_id}
                          onValueChange={(value) =>
                            setNovoItem({ ...novoItem, item_id: value })
                          }
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Selecione um item" />
                          </SelectTrigger>
                          <SelectContent>
                            {itens.map((item) => (
                              <SelectItem
                                key={item.id}
                                value={item.id.toString()}
                              >
                                {item.codigo} - {item.titulo}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="quantidade">Quantidade</Label>
                        <Input
                          id="quantidade"
                          type="number"
                          step="0.001"
                          value={novoItem.quantidade}
                          onChange={(e) =>
                            setNovoItem({
                              ...novoItem,
                              quantidade: e.target.value,
                            })
                          }
                          placeholder="0.000"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="preco_unitario">
                          Preço Unitário (opcional)
                        </Label>
                        <Input
                          id="preco_unitario"
                          type="number"
                          step="0.01"
                          value={novoItem.preco_unitario}
                          onChange={(e) =>
                            setNovoItem({
                              ...novoItem,
                              preco_unitario: e.target.value,
                            })
                          }
                          placeholder="Usar preço padrão"
                        />
                      </div>
                      <Button onClick={adicionarItem} className="w-full">
                        <Plus className="h-4 w-4 mr-2" />
                        Adicionar Item
                      </Button>
                    </CardContent>
                  </Card>

                  {/* Lista de Itens */}
                  <Card className="lg:col-span-2">
                    <CardHeader>
                      <CardTitle>Itens do Orçamento</CardTitle>
                      <CardDescription>
                        Total: {formatarMoeda(orcamentoAtual.total_geral)}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      {itensOrcamento.length === 0 ? (
                        <div className="text-center py-8">
                          <p className="text-gray-600">
                            Nenhum item adicionado
                          </p>
                        </div>
                      ) : (
                        <div className="space-y-4">
                          {itensOrcamento.map((item) => (
                            <div
                              key={item.id}
                              className="border rounded-lg p-4"
                            >
                              <div className="flex justify-between items-start">
                                <div className="flex-1">
                                  <div className="flex items-center space-x-2 mb-2">
                                    <Badge variant="outline">
                                      {item.codigo}
                                    </Badge>
                                    <Badge variant="secondary">
                                      {item.disciplina_nome}
                                    </Badge>
                                  </div>
                                  <h4 className="font-semibold">
                                    {item.titulo}
                                  </h4>
                                  <p className="text-sm text-gray-600 mb-2">
                                    {item.descritivo_tecnico}
                                  </p>
                                  <div className="grid grid-cols-4 gap-4 text-sm">
                                    <div>
                                      <span className="text-gray-500">
                                        Qtd:
                                      </span>{" "}
                                      {item.quantidade} {item.unidade_medida}
                                    </div>
                                    <div>
                                      <span className="text-gray-500">
                                        Unit:
                                      </span>{" "}
                                      {formatarMoeda(item.preco_unitario)}
                                    </div>
                                    <div>
                                      <span className="text-gray-500">
                                        Total:
                                      </span>{" "}
                                      {formatarMoeda(item.preco_total)}
                                    </div>
                                    <div className="text-right">
                                      <Button
                                        size="sm"
                                        variant="destructive"
                                        onClick={() => removerItem(item.id)}
                                      >
                                        <Trash2 className="h-4 w-4" />
                                      </Button>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </div>
              </>
            )}
          </TabsContent>

          {/* Aba Catálogo */}
          <TabsContent value="catalogo" className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-3xl font-bold text-gray-900">
                Catálogo de Itens
              </h2>
            </div>

            <div className="grid gap-6">
              {disciplinas.map((disciplina) => (
                <Card key={disciplina.id}>
                  <CardHeader>
                    <CardTitle>{disciplina.nome}</CardTitle>
                    <CardDescription>{disciplina.descricao}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid gap-4">
                      {itens
                        .filter((item) => item.disciplina_id === disciplina.id)
                        .map((item) => (
                          <div key={item.id} className="border rounded-lg p-4">
                            <div className="flex justify-between items-start">
                              <div className="flex-1">
                                <div className="flex items-center space-x-2 mb-2">
                                  <Badge variant="outline">{item.codigo}</Badge>
                                  <span className="text-sm text-gray-500">
                                    {item.unidade_medida}
                                  </span>
                                </div>
                                <h4 className="font-semibold mb-2">
                                  {item.titulo}
                                </h4>
                                <p className="text-sm text-gray-600 mb-2">
                                  {item.descritivo_tecnico}
                                </p>
                                <p className="text-lg font-semibold text-green-600">
                                  {formatarMoeda(item.preco_unitario_padrao)}
                                </p>
                              </div>
                            </div>
                          </div>
                        ))}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Aba Configurações */}
          <TabsContent value="configuracoes" className="space-y-6">
            <h2 className="text-3xl font-bold text-gray-900">Configurações</h2>

            <Card>
              <CardHeader>
                <CardTitle>Condições Contratuais</CardTitle>
                <CardDescription>
                  Gerencie os modelos de condições contratuais
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {condicoes.map((condicao) => (
                    <div key={condicao.id} className="border rounded-lg p-4">
                      <h4 className="font-semibold">{condicao.nome}</h4>
                      <p className="text-sm text-gray-600">
                        {condicao.descricao}
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}

export default App;
