from openai import OpenAI

client = OpenAI(api_key="test-apy-key")

# Listar modelos disponibles con tu clave
models = client.models.list()

for model in models.data:
    print(model.id)