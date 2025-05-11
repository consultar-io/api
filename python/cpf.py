#!/usr/bin/env python3
"""
Código de exemplo para uso da API de CPF.
Este script demonstra como fazer requisições ao endpoint da API de CPF.
"""

import requests


class CPFAPI:
    """Classe para manipular requisições da API de CPF."""

    def __init__(self, api_token, base_url="https://consultar.io/api/v1"):
        """
        Inicializa o cliente da API de CPF.

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

    def consultar(self, cpf, data_nascimento):
        """
        Consulta informações de CPF.

        Args:
            cpf: Número do CPF (apenas números)
            data_nascimento: Data de nascimento no formato AAAA-MM-DD

        Returns:
            Dados da resposta da API

        Raises:
            requests.exceptions.RequestException: Se a requisição falhar
            ValueError: Se a resposta contiver um erro
        """
        endpoint = f"{self.base_url}/cpf/consultar"
        params = {"cpf": cpf, "data_nascimento": data_nascimento}

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ValueError("CPF não encontrado") from e
            elif response.status_code == 403:
                raise ValueError("Erro de autenticação ou plano inativo") from e
            elif response.status_code == 400:
                raise ValueError("Requisição inválida") from e
            raise


def main():
    """Exemplo de uso da API de CPF."""
    # Substitua pelo seu token de API real
    API_TOKEN = "seu-token-aqui"

    # Inicializa o cliente da API
    cpf_api = CPFAPI(API_TOKEN)

    # CPF e data de nascimento de exemplo
    cpf = "87135740009"
    data_nascimento = "1990-01-01"

    try:
        # Faz a requisição à API
        resultado = cpf_api.consultar(cpf, data_nascimento)

        # Imprime os resultados
        print("\nResultado da consulta CPF:")
        print(f"CPF: {resultado['cpf']}")
        print(f"Nome: {resultado['nome']}")
        print(f"Data de Nascimento: {resultado['data_nascimento']}")
        print(f"Situação: {resultado['situacao']}")
        print(f"Data de Inscrição: {resultado['data_inscricao']}")
        print(f"Dígito Verificador: {resultado['digito_verificador']}")
        print(f"Código de Controle: {resultado['codigo_controle']}")
        print(f"Data de Emissão: {resultado['data_emissao']}")
        print(f"Hora de Emissão: {resultado['hora_emissao']}")
        print(f"QR Code URL: {resultado['qrcode_url']}")

    except ValueError as e:
        print(f"Erro: {str(e)}")
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {str(e)}")


if __name__ == "__main__":
    main()
