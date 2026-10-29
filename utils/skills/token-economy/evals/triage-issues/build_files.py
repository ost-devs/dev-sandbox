"""Builds files/issues.json and truth.json for this case. Run: python3 -I build_files.py

Each component has two bugs, one feature request and one question. Twelve issues get a
duplicate: the same problem told again in other words by another user. The order is
shuffled with a fixed seed; a duplicate always has a higher number than its original.
"""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent

# component: [(type, title, body, duplicate (title, body) or None), ...]
ISSUES = {
    "login": [
        ("bug", "Login com Google volta para a tela inicial", "Clico em 'Entrar com Google', escolho a conta e caio de novo na tela de login, sem mensagem nenhuma. Chrome 130, Windows.",
         ("Não consigo entrar usando a conta Google", "Depois de escolher a conta do Google o sistema me manda de volta pro começo e não loga. Já limpei cache.")),
        ("bug", "Sessão expira em menos de 5 minutos", "Mesmo marcando 'manter conectado', depois de uns 5 minutos parado preciso logar de novo.", None),
        ("feature", "Login com Microsoft", "Boa parte da nossa equipe usa conta Microsoft 365. Seria ótimo ter 'Entrar com Microsoft' além do Google.", None),
        ("question", "Dá para usar o mesmo e-mail em duas empresas?", "Trabalho para dois clientes que usam o sistema. Consigo ter uma conta só com o mesmo e-mail nas duas empresas ou preciso de dois e-mails?", None),
    ],
    "export": [
        ("bug", "CSV exportado quebra acentos no Excel", "Ao abrir o CSV de agendamentos no Excel, 'João' aparece como 'JoÃ£o'. No LibreOffice abre certo.",
         ("Exportação de agendamentos com caracteres estranhos", "Os nomes com acento ficam todos errados quando abro o arquivo exportado no Excel, tipo 'Ã§' no lugar de 'ç'.")),
        ("bug", "Exportação trava com mais de 10 mil linhas", "Com o filtro do ano inteiro (uns 12 mil agendamentos) o botão de exportar fica girando e nunca baixa nada.", None),
        ("feature", "Exportar em XLSX", "Além do CSV, poder baixar direto em .xlsx com as colunas já formatadas ajudaria o financeiro.", None),
        ("question", "Qual o separador do CSV?", "O arquivo exportado usa vírgula ou ponto e vírgula? Preciso configurar a importação no nosso ERP.", None),
    ],
    "email": [
        ("bug", "Lembrete por e-mail chega duas vezes", "Os clientes estão recebendo o lembrete do agendamento em dobro, com um minuto de diferença.",
         ("E-mail de lembrete duplicado", "Toda confirmação de horário está indo repetida para os pacientes. Eles reclamaram que recebem o mesmo aviso 2x.")),
        ("bug", "E-mails de confirmação caindo no spam do Outlook", "Desde semana passada, quase todas as confirmações para endereços @outlook.com vão para a caixa de spam.", None),
        ("feature", "Personalizar o texto do lembrete", "Queria poder editar o texto do e-mail de lembrete, colocar o endereço da clínica e instruções de preparo.", None),
        ("question", "Com quanto tempo de antecedência o lembrete é enviado?", "O e-mail de lembrete sai 24h antes ou no dia? Dá para mudar isso em algum lugar?", None),
    ],
    "search": [
        ("bug", "Busca não encontra nomes com acento", "Procurar 'Conceição' não acha a cliente, mas procurar 'Concei' acha. Parece que o acento atrapalha.",
         ("Pesquisa ignora clientes com til e cedilha", "Se eu digito o nome completo 'Gonçalves' a busca volta vazia, sem acento também não acha. Só funciona com parte do nome.")),
        ("bug", "Busca fica lenta depois de digitar três letras", "A cada letra a tela congela por uns 2 segundos. Temos uns 30 mil clientes cadastrados.", None),
        ("feature", "Buscar por telefone", "Muitos clientes ligam e a gente só tem o número na tela. Poder buscar pelo telefone economizaria muito tempo.", None),
        ("question", "A busca procura também nas observações?", "Se eu escrevi algo no campo de observações do cliente, a busca geral encontra esse texto?", None),
    ],
    "upload": [
        ("bug", "Upload de PDF acima de 5 MB dá erro 413", "Tentei anexar um exame de 7 MB e apareceu 'Erro 413'. O limite informado na tela é 20 MB.", None),
        ("bug", "Foto anexada pelo celular aparece girada", "Fotos tiradas no iPhone e anexadas ao prontuário aparecem deitadas no computador.",
         ("Imagens do iPhone ficam de lado no anexo", "Quando anexo uma foto direto da câmera do iPhone ela fica rotacionada 90 graus na visualização.")),
        ("feature", "Arrastar e soltar arquivos", "Seria prático poder arrastar o arquivo da área de trabalho direto para o agendamento, em vez de clicar em 'Anexar'.", None),
        ("question", "Quais formatos de arquivo posso anexar?", "Posso anexar arquivos .docx e .heic ou só PDF e imagens?", None),
    ],
    "billing": [
        ("bug", "Fatura cobrada duas vezes no cartão", "Neste mês apareceram duas cobranças iguais da assinatura no cartão da empresa, no mesmo dia.", None),
        ("bug", "Nota fiscal sai com CNPJ antigo", "Atualizei o CNPJ nas configurações há dois meses e as notas continuam saindo com o número antigo.",
         ("NF emitida com dados desatualizados da empresa", "Mudamos de CNPJ e já salvei o novo no cadastro, mas a nota fiscal do mês veio de novo com o CNPJ anterior.")),
        ("feature", "Pagamento por Pix", "Queríamos pagar a assinatura por Pix em vez de cartão ou boleto.", None),
        ("question", "Como cancelo a assinatura?", "Não achei a opção de cancelar o plano. É pelo sistema ou preciso falar com o suporte?", None),
    ],
    "dark": [
        ("bug", "Texto invisível no modo escuro na tela de relatórios", "Com o modo escuro ligado, os números das tabelas de relatório ficam pretos sobre fundo preto.", None),
        ("bug", "Modo escuro desliga sozinho ao recarregar", "Ativo o modo escuro, aperto F5 e ele volta para o claro.", None),
        ("feature", "Seguir o tema do sistema operacional", "Seria bom ter a opção 'automático', que segue o claro/escuro do Windows ou macOS.", None),
        ("question", "O modo escuro vale para todos os usuários da conta?", "Se eu ativar o modo escuro, muda para a equipe toda ou só para mim?", None),
    ],
    "android": [
        ("bug", "App Android fecha ao abrir o calendário", "No Android 14 (Samsung S23) o app fecha sozinho assim que toco na aba Calendário.",
         ("Aplicativo trava e sai na aba de agenda", "Uso um Galaxy S23 e toda vez que entro na agenda pelo app ele simplesmente fecha. Reinstalei e continua.")),
        ("bug", "Notificação push não chega no Android", "Não recebo as notificações de novo agendamento no celular, mesmo com tudo permitido nas configurações.", None),
        ("feature", "Widget de agenda do dia", "Um widget na tela inicial do Android mostrando os horários do dia seria muito útil.", None),
        ("question", "Tem versão do app para tablet?", "O app Android funciona bem em tablet ou é só para celular?", None),
    ],
    "calendar": [
        ("bug", "Horário de verão desloca os agendamentos em uma hora", "Clientes de outro fuso estão vendo os horários uma hora adiantados desde a mudança de horário.", None),
        ("bug", "Agendamento recorrente pula o dia 31", "Criei um agendamento mensal para o dia 31 e ele não aparece nos meses que têm 31 dias depois de fevereiro.", None),
        ("feature", "Visão de semana com vários profissionais lado a lado", "Na recepção precisamos ver a semana de 4 profissionais ao mesmo tempo, em colunas.", None),
        ("question", "Como bloqueio um feriado para todos?", "Existe um jeito de bloquear um dia inteiro para todos os profissionais de uma vez, tipo um feriado?", None),
    ],
    "reports": [
        ("bug", "Relatório mensal soma cancelados no faturamento", "O total do relatório de faturamento de setembro inclui agendamentos cancelados.",
         ("Faturamento do relatório está maior que o real", "Conferi o relatório do mês e o valor total conta também as consultas que foram canceladas.")),
        ("bug", "Gráfico de ocupação não carrega no Safari", "No Safari 18 o gráfico de taxa de ocupação fica em branco. No Chrome aparece.", None),
        ("feature", "Agendar envio do relatório por e-mail", "Queria receber o relatório semanal automaticamente toda segunda de manhã no e-mail.", None),
        ("question", "O que conta como 'no-show' no relatório?", "Qual é o critério para um agendamento aparecer como no-show? O cliente precisa ser marcado manualmente?", None),
    ],
    "permissions": [
        ("bug", "Recepcionista consegue ver dados financeiros", "O perfil 'Recepção' está acessando a tela de faturamento, mas nas permissões ela está desmarcada.", None),
        ("bug", "Convite de usuário expira na hora", "Mando o convite para um novo funcionário e o link já abre dizendo 'convite expirado'.", None),
        ("feature", "Perfil de acesso somente leitura", "Precisamos de um perfil para a contabilidade que só consegue ver, sem editar nada.", None),
        ("question", "Quantos usuários posso ter no plano básico?", "O plano básico tem limite de usuários? Quero adicionar mais duas pessoas.", None),
    ],
    "api": [
        ("bug", "Token da API para de funcionar depois de 24h", "Gero o token de API no painel e no dia seguinte todas as chamadas retornam 401, embora a tela diga que não expira.",
         ("API retorna 401 com token que deveria ser permanente", "O token criado como 'sem expiração' começa a dar não autorizado depois de mais ou menos um dia.")),
        ("bug", "Endpoint /appointments ignora o parâmetro de data", "GET /appointments?from=2026-10-01 retorna agendamentos de todas as datas.", None),
        ("feature", "Webhooks para novos agendamentos", "Queremos receber um webhook quando um agendamento é criado ou cancelado, em vez de ficar consultando a API.", None),
        ("question", "Existe limite de chamadas por minuto na API?", "Qual é o rate limit da API? Vamos sincronizar uns 5 mil registros por noite.", None),
    ],
    "gcal": [
        ("bug", "Sincronização com Google Agenda cria eventos duplicados", "Cada agendamento aparece duas ou três vezes no Google Agenda do profissional.", None),
        ("bug", "Cancelamento não remove o evento do Google Agenda", "Quando cancelo um horário no sistema, o evento continua no Google Agenda.", None),
        ("feature", "Sincronizar com o calendário do iPhone", "Além do Google, seria bom sincronizar com o iCloud/Calendário da Apple.", None),
        ("question", "A sincronização com o Google é nos dois sentidos?", "Se eu criar um evento no Google Agenda, ele bloqueia o horário no sistema também?", None),
    ],
    "contacts": [
        ("bug", "Importação de contatos ignora a coluna telefone", "Importei uma planilha com nome, e-mail e telefone; os contatos entraram sem telefone.", None),
        ("bug", "Importação cria clientes duplicados", "Importei a mesma planilha corrigida e cada cliente apareceu duas vezes em vez de atualizar.",
         ("Reimportar a planilha duplica a base de clientes", "Subi de novo o arquivo de contatos com algumas correções e agora tenho todo mundo repetido no cadastro.")),
        ("feature", "Importar contatos do Google", "Poder puxar os contatos direto da conta Google, sem passar por planilha.", None),
        ("question", "Qual modelo de planilha devo usar para importar?", "Tem um modelo de planilha com as colunas certas para a importação de clientes?", None),
    ],
    "i18n": [
        ("bug", "Datas aparecem no formato americano", "Mesmo com o idioma em português, algumas telas mostram as datas como 10/29/2026.", None),
        ("bug", "Botões em inglês na tela de pagamento", "A tela de checkout mostra 'Pay now' e 'Cancel' mesmo com o sistema em português.", None),
        ("feature", "Versão em espanhol", "Vamos abrir uma unidade na Argentina e precisamos do sistema em espanhol.", None),
        ("question", "Cada usuário pode escolher o idioma?", "O idioma é da conta inteira ou cada pessoa pode usar o seu?", None),
    ],
    "dashboard": [
        ("bug", "Dashboard mostra o dia anterior depois da meia-noite", "Entre meia-noite e 3h o painel inicial continua mostrando os agendamentos do dia anterior.", None),
        ("bug", "Contador de agendamentos do dia não atualiza", "O número no card 'Hoje' só muda se eu recarregar a página.",
         ("Card 'Hoje' fica parado no mesmo número", "Os novos agendamentos entram, mas o total do dia na tela inicial não muda até eu dar refresh.")),
        ("feature", "Escolher quais cards aparecem no dashboard", "Gostaria de esconder os cards que não uso e reorganizar os outros.", None),
        ("question", "De onde vem a 'taxa de retorno' do dashboard?", "Como é calculada a taxa de retorno que aparece no painel?", None),
    ],
    "password": [
        ("bug", "E-mail de redefinição de senha não chega", "Peço para redefinir a senha e o e-mail nunca chega, nem no spam.",
         ("Não recebo o link de recuperação de senha", "Cliquei em 'esqueci minha senha' várias vezes e nenhuma mensagem apareceu na minha caixa de entrada.")),
        ("bug", "Senha com caractere especial não é aceita no login", "Minha senha tem '&' e o login diz que está errada, mas ela foi aceita no cadastro.", None),
        ("feature", "Autenticação em dois fatores", "Precisamos de 2FA por aplicativo autenticador para atender a política de segurança da empresa.", None),
        ("question", "Qual é a regra mínima de senha?", "Quantos caracteres e que tipos a senha precisa ter?", None),
    ],
}


def main():
    originals, dups = [], []
    for comp, items in ISSUES.items():
        for typ, title, body, dup in items:
            key = (comp, title)
            originals.append({"key": key, "type": typ, "title": title, "body": body})
            if dup:
                dups.append({"key": key, "type": typ, "title": dup[0], "body": dup[1], "dup_of": key})
    assert len(originals) == 68 and len(dups) == 12
    r = random.Random(42)
    r.shuffle(originals)
    r.shuffle(dups)
    # duplicates go after their originals: insert each at a random later position
    order = list(originals)
    for d in dups:
        pos = next(i for i, o in enumerate(order) if o.get("key") == d["dup_of"] and "dup_of" not in o)
        order.insert(r.randint(pos + 1, len(order)), d)
    users = ["ana.lima", "bruno.s", "carla_m", "dioguinho", "erica.p", "fabio.r", "gabi", "heitor.c", "isa.n", "joao.v"]
    number_of, issues, truth = {}, [], {}
    for i, it in enumerate(order, start=101):
        if "dup_of" not in it:
            number_of[it["key"]] = i
        issues.append({"number": i, "title": it["title"], "body": it["body"], "user": r.choice(users),
                       "created_at": f"2026-{9 + i // 150:02d}-{1 + (i * 7) % 28:02d}"})
        truth[i] = {"type": it["type"], "dup_of": None}
    for i, it in enumerate(order, start=101):
        if "dup_of" in it:
            truth[i]["dup_of"] = number_of[it["dup_of"]]
            assert truth[i]["dup_of"] < i
    files = HERE / "files"
    files.mkdir(exist_ok=True)
    (files / "issues.json").write_text(json.dumps(issues, ensure_ascii=False, indent=1) + "\n")
    (HERE / "truth.json").write_text(json.dumps(truth, indent=1) + "\n")
    print(len(issues), "issues,", sum(1 for t in truth.values() if t["dup_of"]), "duplicates")


if __name__ == "__main__":
    main()
