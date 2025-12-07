import logoImg from "../../assets/logoSite.png"
import exemplo from "../../assets/ft.jpg"

function Appointment(){

    const listAppointments = [
        {
            id: 1,
            barberName: "Felipe",
            contact: "(88) 99999-1111",
            date: "12/12/2025",
            time: "14:30h",
            services: "Barba e cabelo",
            image: exemplo 
        },
        {
            id: 2,
            barberName: "João",
            contact: "(88) 99999-2222",
            date: "13/12/2025",
            time: "09:00h",
            services: "Corte Social",
            image: exemplo
        },
        {
            id: 3,
            barberName: "Carlos",
            contact: "(88) 99999-3333",
            date: "13/12/2025",
            time: "10:00h",
            services: "Barba",
            image: exemplo
        }

    ]
    
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
                       {listAppointments.map((item)=>(
                        <li>
                            <div className={item.barberName}>
                                <img src={item.image} alt="logo site" width={150}/>
                                <p className="name">
                                    <span>Barbeiro:</span> {item.barberName}
                                </p>
                                <p className="contact">
                                    <span>Barbeiro:</span> {item.contact}
                                </p>
                                <p className="date">
                                    <span>Data:</span> {item.date}
                                </p>
                                <p className="time">
                                    <span>Horário:</span> {item.time}
                                </p>
                                <p className="services">
                                </p>
                            </div>
                        </li>
                       ))}
                    </ol>
                </div>
            </div>
        </div>
        </>
    )
}

export default Appointment