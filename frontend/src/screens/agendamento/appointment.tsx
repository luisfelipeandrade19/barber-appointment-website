import logoImg from "../../assets/logoSite.png"
import exemplo from "../../assets/ft.jpg"

function Appointment(){

    
    return(
        <>
        <div className="container">
            <header>
                <img src={logoImg} alt="logo site" />
            </header>
            <div className="content-main">
                <button>AGENDAR AGORA</button>
                <div className="appoiments">
                    <h1>Meus Agendamentos:</h1>
                    <ol id="appoiments-list">
                        <li>
                            <div className="barber01">
                                <img src={exemplo} alt="logo site" width={150}/>
                                <p className="name">
                                    <span>Barbeiro:</span> Felipe
                                </p>
                                <p className="contact">
                                    <span>Barbeiro:</span> (88) 00000-0000
                                </p>
                                <p className="date">
                                    <span>Data:</span> xx/xx/xxxx
                                </p>
                                <p className="time">
                                    <span>Horário:</span> 00:00h
                                </p>
                                <p className="services">
                                    <span>Serviços:</span> Barba e cabelo
                                </p>
                            </div>
                        </li>
                    </ol>
                </div>
            </div>
        </div>
        </>
    )
}

export default Appointment