#!/usr/bin/env python3
"""
Código de exemplo para uso da API de CNPJ.
Este script demonstra como fazer requisições ao endpoint da API de CNPJ.
"""

import requests


class CNPJAPI:
    """Classe para manipular requisições da API de CNPJ."""

    def __init__(self, api_token, base_url="https://consultar.io/api/v1"):
        """
        Inicializa o cliente da API de CNPJ.

        Args:
            api_token: Seu token de API para autenticação
            base_url: URL base da API
        """
        self.api_token = api_token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json",
        }

    def consultar(self, cnpj):
        """
        Consulta informações de CNPJ.

        Args:
            cnpj: Número do CNPJ (14 dígitos)

        Returns:
            Dados da resposta da API

        Raises:
            requests.exceptions.RequestException: Se a requisição falhar
            ValueError: Se a resposta contiver um erro
        """
        endpoint = f"{self.base_url}/cnpj/consultar"
        params = {"cnpj": cnpj}

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ValueError("CNPJ não encontrado") from e
            elif response.status_code == 403:
                raise ValueError("Erro de autenticação ou plano inativo") from e
            elif response.status_code == 400:
                raise ValueError("Requisição inválida") from e
            raise


def format_cnpj_info(resultado):
    """
    Formata e imprime as informações do CNPJ de forma legível.

    Args:
        resultado: Dados da resposta da API
    """
    print("\nInformações Básicas:")
    print(f"CNPJ: {resultado['cnpj_formatado']}")
    print(f"Razão Social: {resultado['razao_social']}")
    print(f"Nome Fantasia: {resultado['nome_fantasia']}")
    print(f"Natureza Jurídica: {resultado['natureza_juridica_descricao']}")
    print(f"Capital Social: {resultado['capital_social_formatado']}")
    print(f"Porte: {resultado['porte_empresa_descricao']}")
    print(f"Matriz/Filial: {resultado['matriz_filial_descricao']}")
    print(f"Situação Cadastral: {resultado['situacao_cadastral_descricao']}")
    print(f"Data da Situação: {resultado['data_situacao_cadastral']}")
    print(f"Motivo da Situação: {resultado['motivo_situacao_cadastral_descricao']}")
    print(f"Data de Abertura: {resultado['data_inicio_atividades']}")

    print("\nEndereço:")
    print(f"Tipo de Logradouro: {resultado['tipo_logradouro']}")
    print(f"Logradouro: {resultado['logradouro']}")
    print(f"Número: {resultado['numero']}")
    print(f"Complemento: {resultado['complemento']}")
    print(f"Bairro: {resultado['bairro']}")
    print(f"Cidade: {resultado['municipio_descricao']}")
    print(f"UF: {resultado['uf']}")
    print(f"CEP: {resultado['cep']}")

    print("\nContato:")
    if resultado["ddd1"] and resultado["telefone1"]:
        print(f"DDD: {resultado['ddd1']}")
        print(f"Telefone: {resultado['telefone1']}")
    if resultado["ddd2"] and resultado["telefone2"]:
        print(f"DDD 2: {resultado['ddd2']}")
        print(f"Telefone 2: {resultado['telefone2']}")
    if resultado["ddd_fax"] and resultado["fax"]:
        print(f"DDD Fax: {resultado['ddd_fax']}")
        print(f"Fax: {resultado['fax']}")
    print(f"Email: {resultado['email']}")

    print("\nAtividade Principal:")
    print(f"Código CNAE: {resultado['cnae_principal_codigo']}")
    print(f"Descrição CNAE: {resultado['cnae_principal_descricao']}")

    if resultado["lista_cnae_secundarios"]:
        print("\nAtividades Secundárias:")
        for cnae in resultado["lista_cnae_secundarios"]:
            print(f"Código: {cnae['codigo']}")
            print(f"Descrição: {cnae['descricao']}")

    if resultado["lista_qsa"]:
        print("\nQuadro Societário:")
        for socio in resultado["lista_qsa"]:
            print(f"\nSócio: {socio['nome_qsa']}")
            print(f"Tipo: {socio['tipo_qsa_descricao']}")
            print(f"CPF/CNPJ: {socio['cpf_cnpj_qsa_formatado']}")
            print(f"Qualificação: {socio['qualificacao_qsa_descricao']}")
            print(f"Data de Entrada: {socio['data_entrada_qsa']}")
            if socio["faixa_etaria_qsa_descricao"]:
                print(f"Faixa Etária: {socio['faixa_etaria_qsa_descricao']}")


def main():
    """Exemplo de uso da API de CNPJ."""
    # Substitua pelo seu token de API real
    API_TOKEN = "seu-token-aqui"

    # Inicializa o cliente da API
    cnpj_api = CNPJAPI(API_TOKEN)

    # CNPJ de exemplo
    cnpj = "42515236000100"

    try:
        # Faz a requisição à API
        resultado = cnpj_api.consultar(cnpj)

        # Formata e imprime os resultados
        format_cnpj_info(resultado)

    except ValueError as e:
        print(f"Erro: {str(e)}")
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {str(e)}")


if __name__ == "__main__":
    main()
