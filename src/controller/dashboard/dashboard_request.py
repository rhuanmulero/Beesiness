from flask import Blueprint, render_template, request, abort, session
from flask_login import login_required, current_user
from src import cache


from src.controller.dashboard.company.info_authorization import info_authorization
from src.controller.dashboard.company.info_assets import info_assets
from src.controller.dashboard.company.info_journal import info_journal
from src.controller.dashboard.company.info_balance import info_balance
from src.controller.dashboard.company.info_razonete import info_razonete
from src.controller.dashboard.company.info_dashboard import info_dashboard
from src.controller.dashboard.company.info_liabilities import info_liabilities
from src.controller.dashboard.user.info_user_companies import info_user_companies

from src.controller.dashboard.company.register_asset import asset_registration
from src.controller.dashboard.company.register_liability import liability_registration

from src.model.database.company.companies.search import db_search_company
from src.model.database.company.user_companies.search import db_search_user_company
from src.model.database.company.user_companies.search_users import db_search_users_in_company



# Tudo aqui no url é: /dashboard, ou seja: 127.0.0.1:5000/dashboard/...

dashboard_request = Blueprint('auth_dashboard', __name__, template_folder='templates', static_folder='static')

#----------------------------------------------------------------------------------------- DASHBOARD DO USUÁRIO

@dashboard_request.route('/user', methods=['POST','GET']) 
@login_required
def dashboard_user():
    if request.method == 'POST':
        return info_user_companies()
    
    if request.method == 'GET':
        return render_template('dashboard/user/dashboard.html')

#----------------------------------------------------------------------------------------- DASHBOARD DA EMPRESA


@dashboard_request.route(f'/company/<cnpj>', methods=['POST','GET']) 
@login_required
def dashboard_company(cnpj):
    if request.method == 'POST':
        company_id = session.get('company_id')
        return info_dashboard(company_id)
    
    if request.method == 'GET':
        validate_cnpj_access(cnpj)
        return render_template('dashboard/company/dashboard.html', cnpj=cnpj)

#----------------------------------------------------------------------------------------- REGISTRO DE ATIVOS

@dashboard_request.route(f'/register/asset/<cnpj>', methods=['POST','GET']) 
@login_required
def register_asset_site(cnpj):
    if request.method == 'POST':
        asset_data = request.get_json()
        company_id = session.get('company_id')

        return asset_registration(asset_data, company_id)
    if request.method == 'GET':
        validate_cnpj_access(cnpj);
        return render_template('dashboard/company/assets/register.html', cnpj=cnpj)

#----------------------------------------------------------------------------------------- REGISTRO DE PASSIVOS


@dashboard_request.route(f'/register/liability/<cnpj>', methods=['POST','GET']) 
@login_required
def register_liability_site(cnpj):
    if request.method == 'POST':
        liability_data = request.get_json()
        company_id = session.get('company_id')
    
        return liability_registration(liability_data, company_id)
    if request.method == 'GET': 
        validate_cnpj_access(cnpj);
        return render_template('dashboard/company/liabilities/register.html', cnpj=cnpj)
    
#----------------------------------------------------------------------------------------- LIVRO DE RAZÃO (EXTRATO)

@dashboard_request.route('/journal/<cnpj>', methods=['POST','GET'])
@login_required
def register_journal_site(cnpj): 
    if request.method == 'POST':
        company_id = session.get('company_id')
        return info_journal(company_id, cnpj)

    if request.method == 'GET': 
        validate_cnpj_access(cnpj)
        return render_template('dashboard/company/reports/journal.html',cnpj=cnpj)
    

#----------------------------------------------------------------------------------------- BALANÇO PATRIMONIAL

@dashboard_request.route('/balance/<cnpj>', methods=['POST','GET'])
@login_required
def balance_site(cnpj): 
    if request.method == 'POST':
        company_id = session.get('company_id')
        return info_balance(company_id, cnpj)

    if request.method == 'GET': 
        validate_cnpj_access(cnpj)
        return render_template('dashboard/company/reports/balance.html',cnpj=cnpj)


#----------------------------------------------------------------------------------------- RAZONETE

@dashboard_request.route('razonete/<cnpj>', methods=['POST','GET'])
@login_required
def razonete_site(cnpj): 
    if request.method == 'POST':
        company_id = session.get('company_id')
        return info_razonete(company_id, cnpj)

    if request.method == 'GET': 
        validate_cnpj_access(cnpj)
        return render_template('dashboard/company/reports/razonete.html', cnpj=cnpj)

#----------------------------------------------------------------------------------------- RESUMO DE ATIVO E PASSIVO

@dashboard_request.route('<cnpj>/<type>/<uuid>', methods=['POST','GET'])
@login_required
def asset_information(cnpj, type, uuid):
    if request.method == 'GET': 
        print('entrou no asset_information')
        validate_cnpj_access(cnpj)
        
        # Se formos fazer desta forma mesmo, temos algumas coisas para resolver: 
        # 1. O db_search_liability e db_search_asset busca apenas o uuid de empresas e esse uuid é do asset ou liability, precisamos mudar o código de search do banco de dados.
        # 2. Caso info não exista, provavelmente dará erro, podemos fazer um if e elif para evitar que isso ocorra, se existir dado: manda pra página, se não houver: ?
        
        return render_template('dashboard/company/reports/info_reason.html')

#-----------------------------------------------------------------------------------------

@dashboard_request.route('assets/<cnpj>', methods=['POST','GET'])
@login_required
def assets_site(cnpj): 
    if request.method == 'POST':
        company_id = session.get('company_id')
        return info_assets(company_id)

    if request.method == 'GET': 
        validate_cnpj_access(cnpj)
        return render_template('dashboard/company/assets/assets.html',cnpj=cnpj)

#-----------------------------------------------------------------------------------------
#   
@dashboard_request.route('liabilities/<cnpj>', methods=['POST','GET'])
@login_required
def liabilities_site(cnpj): 
    if request.method == 'POST':
        company_id = session.get('company_id')
        return info_liabilities(company_id)

    if request.method == 'GET': 
        validate_cnpj_access(cnpj)
        return render_template('dashboard/company/liabilities/liabilities.html',cnpj=cnpj)


#-----------------------------------------------------------------------------------------

@dashboard_request.route('/company/<cnpj>/authorization', methods=['POST','GET'])
@login_required
def authorization_site(cnpj):
    company_id = session.get('company_id')

    if request.method == 'POST':
        data = request.get_json()
        company_id = session.get('company_id')
        return info_authorization(data, company_id)
    
    if request.method == 'GET':
        validate_creator_access(cnpj)
        users = db_search_users_in_company(company_id)

        return render_template('dashboard/company/authorization/authorization.html', users=users)
    
#-----------------------------------------------------------------------------------------

@dashboard_request.route('/company/<cnpj>/settings', methods=['POST','GET'])
@login_required
def settings_site(cnpj):
    company_id = session.get('company_id')

    if request.method == 'POST':
        data = request.get_json()
        company_id = session.get('company_id')
        #return info_authorization(data, company_id)
    
    if request.method == 'GET':
        validate_creator_access(cnpj)

        return render_template('dashboard/company/settings.html')


def validate_cnpj_access(cnpj):
    # Estas verificações são necessárias para que os usuários não burlem as empresas pelo URL.
    # Erro 404 - Página não encontrada
    # Erro 403 - Falta de permissão para acesso.

    # Verifica se o CNPJ na URL tem 14 caracteres
    if len(cnpj) != 14:
        abort(404)

    cached_relation = cache.get(f'relation_{current_user.id}_{cnpj}')
    if cached_relation:
        company_id, user_access_level = cached_relation
    else:
        company = db_search_company(cnpj)
        if not company:
            abort(404)

        user_company_relation = db_search_user_company(current_user.id, company[0][0])
        if not user_company_relation:
            abort(403)

        # Desestrutura a array para pegar o company_id, user_id e o nível de acesso
        company_id, user_id, user_access_level, id = user_company_relation[0]

        # Armazena a relação do usuário no cache
        cache.set(f'relation_{current_user.id}_{cnpj}', (company_id, user_access_level), timeout=600)

    if user_access_level not in ['creator', 'editor', 'checker', 'viewer']:
        abort(403)

    session['company_id'] = company_id

def validate_creator_access(cnpj):
    cached_relation = cache.get(f'relation_{current_user.id}_{cnpj}')
    
    if not cached_relation:
        validate_cnpj_access(cnpj)
        cached_relation = cache.get(f'relation_{current_user.id}_{cnpj}')

    company_id, user_access_level = cached_relation

    if user_access_level != 'creator':
        abort(403)

    # Armazena o company_id na sessão
    session['company_id'] = company_id
