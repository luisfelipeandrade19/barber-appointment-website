function Agendar(){

    return(
        <>
      <div className="container">
        <header>
          <h1>Agendamento de serviço</h1>
        </header>

        <div className="form-group">

    <label>Barbeiro:</label>
    <select className="input-field">
        <option value="" disabled selected>Selecione um barbeiro</option>
        <option value="barbeiro1">Matheus Bombeiro</option>
    </select>
</div>

<div className="form-group">
    <label>Serviços:</label>
    <select className="input-field">
        <option value="" disabled selected>Escolha o serviço</option>
        <option value="corte">Corte Social</option>
        <option value="barba">Barba Completa</option>
        <option value="combo">Corte + Barba</option>
    </select>
</div>

<div className="form-group">
    <label>Data:</label>
    <input type="date" className="input-field" id="data-agendamento"/>
</div>

<div className="form-group">
  <label>Horários disponíveis:</label>
  <select className="input-field">
    <option value="" disabled selected>Selecione um horário</option>
    <option value="09:00">09:00</option>
    <option value="09:30">09:30</option>
    <option value="10:00">10:00</option>
    <option value="10:30">10:30</option>
    <option value="11:00">11:00</option>
    <option value="11:30">11:30</option>
    <option value="12:00">12:00</option>
  </select>
</div>

      </div>
        </>
    )
}

export default Agendar;