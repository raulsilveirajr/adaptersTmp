# pocGenericDataSync

Uma POC de um datasync genérico configurável via JSON.

## Virtual Enviroment Inicialization
python3 -m venv .venv
# To activate
source ./.venv/bin/activate
# To deactivate
deactivate

## Pré-requisitos

- Python 3.x
- [Poetry](https://python-poetry.org/)

## Instalação

1. Clone o repositório:

   ```bash
   git clone git@github.com:raulsilveirajr/pocGenericDataSync.git
   cd pocGenericDataSync
   ```

2. Instale as dependências do projeto usando o Poetry:

   ```bash
   poetry install
   ```

## Executando o Projeto

Para rodar o projeto e passar a string "accounts" como parâmetro, use o seguinte comando:

```bash
python main.py accounts
```

## Subindo o servidor (o usuário deve ter permissão para rodar o servidor como root)

```bash
python webhook.py
```

## Exemplo de requisição para o servidor

curl --request POST \
  --url http://localhost/webhook/accounts \
  --header 'content-type: application/json' \
  --data '[ 
  {
    "cliente": "CB000000",
    "sociedad": "BO99",
    "persona_fisica": null,
    "grupo_cuentas": null,
    "codigo_pais": "BO",
    "nombre_pais": "BOLIVIA",
    "nombre": "ARIEL",
    "calle": " ",
    "poblacion": "COCHABAMBA",
    "region": "COCHABAMBA",
    "telefono_1": 76919294,
    "direccion": "AVENIDA CHAPARE",
    "tratamiento": null,
    "creado_el": 20231126,
    "creado_por": "test",
    "distrito": null,
    "tipo_nif": 401,
    "texto": "CI - CÉDULA DE IDENTIDAD",
    "n_ident_fis_1": 76999999,
    "zona_transporte": null,
    "texto_zona_transporte": null,
    "lista_precios": "BM11BO010141",
    "denominacion": "Distribuidor",
    "organiz_ventas": 8110,
    "canal_distrib": 41,
    "sector": 1,
    "esquema_cliente": null,
    "grupo_clientes": "RUBI -",
    "moneda": "BOB",
    "texto_moneda": "BOLIVIANO",
    "gpo_imputacion": null,
    "texto_de_gpo_imputacion": null,
    "centro_sumin": "BM11",
    "zona_de_ventas": "BO0101",
    "oficina_ventas": "BO10",
    "texto_oficina_ventas": "Cochabamba",
    "clasificacion_de_clientes": "TNEGOCIO2",
    "texto_de_clasificacion_de_clientes": "TIENDA DE BARRIO",
    "telefono": 76999999,
    "n_telefono": 76999999,
    "codigo_persona_de_contacto": null,
    "nombre_persona_de_contacto": null,
    "condicion_de_pago": "Z000",
    "texto_condicion_de_pago": "CONTADO",
    "distrito_1": null,
    "correo": null,
    "grupo_precios": null,
    "grupo_vendedores": null,
    "latitud": -00.000000,
    "longitud": -00.000000,
    "clasificacion_fiscal_cliente": null,
    "minimo_metodo_pago": "Z000",
    "minimo_compra": 460.0,
    "challengeID": "CB000000",
    "número_de_calle": 0,
    "codigo_postal": null,
    "state": "COCHABAMBA",
    "nombre_legal": "ARIEL",
    "correo_del_propietario": null,
    "nombre_del_propietario": "ARIEL",
    "apellido_del_propietario": "ARIEL",
    "telefono_del_propietario": 76999999,
    "dias_de_pago": 0,
    "estatus": "VIGENTE",
    "nombre_del_representante": "BEL ORDOÑEZ",
    "rol_del_representante": "SR.",
    "telefono_del_representante": 4200000,
    "codigo_de_mercado": "BO0101"
  }
]
'