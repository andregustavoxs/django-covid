
window.onload = function() {

  let inicio = new Date()

  let segundoInicio = inicio.getSeconds()

  let fim = new Date()

  let segundoFim = fim.getSeconds()

  while (segundoFim - segundoInicio < 5) {

    let fim = new Date()

    segundoFim = fim.getSeconds()

  }

  const mensagem = document.getElementsByClassName("erro")[0]

  if (mensagem) mensagem.style.setProperty('display', 'none')

}