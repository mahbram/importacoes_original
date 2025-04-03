document.addEventListener("DOMContentLoaded", function () {
    let criarGrupoBtn = document.getElementById("criarGrupoBtn");

    if (criarGrupoBtn) {
        criarGrupoBtn.addEventListener("click", function () {
            fetch("/obter_sequencial")
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Erro HTTP: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    let proximoGrupoElem = document.getElementById("proximoGrupo");
                    let novoGrupoInputElem = document.getElementById("novoGrupoInput");
                    let tituloElem = document.getElementById("titulo");
                    let codigoElem = document.getElementById("codigo");
                    let descricaoElem = document.getElementById("descricao");

                    if (data.proximo_grupo) {
                        if (proximoGrupoElem) {
                            proximoGrupoElem.innerText = `Próximo Grupo: ${data.proximo_grupo}`;
                        } else {
                            console.warn("Elemento 'proximoGrupo' não encontrado.");
                        }

                        if (novoGrupoInputElem) {
                            novoGrupoInputElem.value = data.proximo_grupo;
                        } else {
                            console.warn("Campo de input 'novoGrupoInput' não encontrado.");
                        }

                        // Habilita os campos de edição
                        if (tituloElem) tituloElem.removeAttribute("disabled");
                        if (codigoElem) codigoElem.removeAttribute("disabled");
                        if (descricaoElem) descricaoElem.removeAttribute("disabled");

                        // Preenche os campos com dados iniciais
                        if (tituloElem) tituloElem.value = `Grupo ${data.proximo_grupo}`;
                        if (codigoElem) codigoElem.value = `RC_NRM_1_${data.proximo_grupo}`;
                    } else {
                        console.error("Erro ao obter o próximo grupo:", data.erro);
                    }
                })
                .catch(error => {
                    console.error("Erro na requisição:", error);

                    let proximoGrupoElem = document.getElementById("proximoGrupo");
                    if (proximoGrupoElem) {
                        proximoGrupoElem.innerText = "Erro ao carregar o próximo grupo.";
                    }
                });
        });
    } else {
        console.warn("Botão 'criarGrupoBtn' não encontrado.");
    }
});





$.ajax({
    url: 'http://127.0.0.1:5000/obter_sequencial',
    method: 'GET',
    success: function(data) {
        console.log(data.sequencial);
    },
    error: function() {
        console.error('Erro ao carregar sequencial.');
    }
});







document.getElementById("formGrupo").addEventListener("submit", function (e) {
    e.preventDefault(); // Impede o recarregamento da página
    
    let titulo = document.getElementById("titulo").value;
    let codigo = document.getElementById("codigo").value;
    let descricao = document.getElementById("descricao").value;

    if (!titulo || !codigo || !descricao) {
        alert("Preencha todos os campos!");
        return;
    }

    $.ajax({
        url: "/salvar_grupo",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ 
            titulo: titulo, 
            codigo: codigo, 
            descricao: descricao 
        }),
        success: function (data) {
            alert("Grupo salvo: " + data.grupo);
            $("#modalGrupo").modal("hide");
        },
        error: function (error) {
            alert("Erro ao salvar.");
            console.error(error);
        }






    });
});

document.getElementById('upload forms').reset();




