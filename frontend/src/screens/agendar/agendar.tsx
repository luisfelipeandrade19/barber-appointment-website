import { useState } from "react";
import BarberFormGroup from "../../lib/components/barberFormGroup/barberFormGroup";
import "./agendar.css";
import ServicesFormGroup from "../../lib/components/servicesFormGroup/servicesFormGroup";
import { useNavigate } from "react-router-dom";
import TimeFormGroup from "../../lib/components/timeFormGroup/timeFormGroup";

function Agendar() {
  const [selectedBarberId, setSelectedBarberId] = useState("");
  const [selectedServiceId, setSelectedServiceId] = useState("");
  const [selectedData, setSelectedData] = useState("")

  const [selectedTime, setSelectedTime] = useState("")

  const navigate = useNavigate()

  const [loading, setLoading] = useState(false)

  const usuarioLogado = localStorage.getItem('usuario');
  const ID_CLIENTE = usuarioLogado ? JSON.parse(usuarioLogado).id : null;

  const handleAgendar = async () => {
    if (!ID_CLIENTE) {
      alert("Você precisa estar logado para agendar.");
      navigate('/');
      return;
    }

    if (!selectedBarberId || !selectedServiceId || !selectedData || !selectedTime) {
      alert("Por favor, preencha todos os campos.");
      return;
    }

    setLoading(true)

    try {
      const dateTimeString = `${selectedData}T${selectedTime.split('T')[1]}`;
      const response = await fetch('/api/agendamentos', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id_cliente: ID_CLIENTE,
          id_barbeiro: parseInt(selectedBarberId),
          servicos: [parseInt(selectedServiceId)],
          data_hora: dateTimeString
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || "Erro ao fazer agendamento!")
      }

      navigate('/agendamentos')

    } catch (error) {
      console.error("Erro na requisicao", error)
      alert("Erro ao realizar agendamento: ")
    } finally {
      setLoading(false)
    }
  }

  const handleBarberSelect = (id: string) => {
    console.log("Barbeiro selecionado no pai:", id);
    setSelectedBarberId(id);
    setSelectedServiceId("");
  };
  const handleServiceSelect = (id: string) => {
    console.log("Serviço selecionado:", id);
    setSelectedServiceId(id);
  };
  const handleDataSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    console.log("Data selecionada:", value)
    setSelectedData(value)
  }
  const handleTimeSelect = (time: string) => {
    console.log("Horário selecionado:", time);
    setSelectedTime(time);
  }


  return (
    <>
      <div className="agendar-container">
        <header className="agendar-header">
          <h1>Agendamento de serviço</h1>
        </header>

        <div className=" form-group">
          {/* Removed onChange prop as it is not defined in BarberFormGroupProps */}
          <BarberFormGroup onSelect={handleBarberSelect} />

          <ServicesFormGroup
            barbeiro_id={selectedBarberId}
            onSelect={handleServiceSelect}
          />

          <div className="date-form-group" id="forms">
            <label>Data:</label>
            <input type="date" className="input-field" id="data-agendamento" onChange={handleDataSelect} />
          </div>

          <TimeFormGroup date={selectedData} id_barbeiro={selectedBarberId} onSelect={handleTimeSelect} />

          <div className="button-app">
            <button className="appointment-page-btn" id="btn-appoint" onClick={handleAgendar} disabled={loading}>
              {loading ? "AGENDANDO..." : "AGENDAR AGORA"}
            </button>
          </div>
        </div>

      </div>
    </>
  )
}

export default Agendar;