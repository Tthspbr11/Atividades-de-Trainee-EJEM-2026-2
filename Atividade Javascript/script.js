const API = "https://pokeapi.co/api/v2";

const campo = document.getElementById("campo");
const botao = document.getElementById("botao");
const mensagem = document.getElementById("mensagem");
const cartao = document.getElementById("cartao");
const sprite = document.getElementById("sprite");
const nomeEl = document.getElementById("nome");
const tiposEl = document.getElementById("tipos");

// a API devolve os tipos em inglês, então traduzi pra ficar em português
const tiposPt = {
  normal: "Normal", fire: "Fogo", water: "Água", electric: "Elétrico",
  grass: "Planta", ice: "Gelo", fighting: "Lutador", poison: "Veneno",
  ground: "Terrestre", flying: "Voador", psychic: "Psíquico", bug: "Inseto",
  rock: "Pedra", ghost: "Fantasma", dragon: "Dragão", dark: "Sombrio",
  steel: "Aço", fairy: "Fada"
};

const coresTipos = {
  normal: "#8a8a6a", fire: "#e0662b", water: "#3f7fd4", electric: "#c9a20f",
  grass: "#4c9a3a", ice: "#5aaeb0", fighting: "#b02a22", poison: "#8e3a8e",
  ground: "#b8943f", flying: "#7a8fd8", psychic: "#d9487a", bug: "#8a9a14",
  rock: "#9a8528", ghost: "#5f4a8a", dragon: "#5a30d8", dark: "#5c4a3c",
  steel: "#7e7e96", fairy: "#d47a95"
};

function mostrarMensagem(texto, ehErro) {
  mensagem.textContent = texto;
  mensagem.className = ehErro ? "erro" : "";
}

// deixa o texto no formato que a API entende:
// "Mr. Mime" -> "mr-mime", "Farfetch'd" -> "farfetchd", "Nidoran♀" -> "nidoran-f"
function normalizar(texto) {
  return texto
    .trim()
    .toLowerCase()
    .replace("♀", "-f")
    .replace("♂", "-m")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "") // tira acentos
    .replace(/[.'’:]/g, "")
    .replace(/\s+/g, "-");
}

// devolve o JSON, ou null se a API responder 404
async function pegarJson(url) {
  const resposta = await fetch(url);
  if (resposta.status === 404) return null;
  if (!resposta.ok) throw new Error("Erro " + resposta.status);
  return resposta.json();
}

// alguns pokémon (deoxys, giratina, wormadam...) não existem em /pokemon/nome,
// só em /pokemon-species/nome, então tentamos os dois
async function acharPokemon(nome) {
  const direto = await pegarJson(API + "/pokemon/" + nome);
  if (direto) return direto;

  const especie = await pegarJson(API + "/pokemon-species/" + nome);
  if (especie) {
    const padrao = especie.varieties.find(function (v) {
      return v.is_default;
    }) || especie.varieties[0];
    return pegarJson(padrao.pokemon.url);
  }

  return null;
}

function mostrarPokemon(dados) {
  // imagem oficial; se não tiver, cai no sprite normal
  const artwork = dados.sprites.other && dados.sprites.other["official-artwork"];
  const imagem = (artwork && artwork.front_default) || dados.sprites.front_default;

  const tipos = dados.types.map(function (t) {
    return t.type.name;
  });

  sprite.src = imagem;
  sprite.alt = "Imagem oficial de " + dados.name;
  nomeEl.textContent = dados.name.replace(/-/g, " ");

  tiposEl.innerHTML = "";
  tipos.forEach(function (tipo) {
    const li = document.createElement("li");
    li.textContent = tiposPt[tipo] || tipo;
    tiposEl.appendChild(li);
  });

  cartao.style.setProperty("--cor", coresTipos[tipos[0]] || "#8a8a6a");
  cartao.hidden = false;
}

async function buscarPokemon() {
  const nome = normalizar(campo.value);

  cartao.hidden = true;

  if (nome === "") {
    mostrarMensagem("Digite o nome de um Pokémon primeiro.", true);
    return;
  }

  botao.disabled = true;
  mostrarMensagem("Buscando...", false);

  try {
    const dados = await acharPokemon(nome);

    if (!dados) {
      mostrarMensagem('Pokémon "' + nome + '" não encontrado.', true);
      return;
    }

    mostrarPokemon(dados);
    mostrarMensagem("", false);
  } catch (erro) {
    console.error(erro);
    mostrarMensagem("Não deu pra buscar agora. Verifique sua conexão e tente de novo.", true);
  } finally {
    botao.disabled = false;
  }
}

botao.addEventListener("click", buscarPokemon);
campo.addEventListener("keydown", function (e) {
  if (e.key === "Enter") buscarPokemon();
});
