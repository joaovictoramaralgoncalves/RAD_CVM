@echo off

python limpeza_memoria_e_cache.py

call .\env\Scripts\activate

if defined VIRTUAL_ENV (
    echo Estou dentro do ambiente virtual.
) else (
    echo Não estou dentro do ambiente virtual.
)

python limpeza_memoria_e_cache.py

python Execucao.py

timeout /t 15


