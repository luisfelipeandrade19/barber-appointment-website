import voltar from "../../assets/volte.png"
import exemplo from "../../assets/foto-do-perfil.png"


interface BarberHistoryItem {
    id: number;
    barberName: string;
    contact: string;
    email: string;
    date: string;
    services: string;
    image: string; // ou StaticImageData se usar Next.js
}

function HistoryPage(){

    const listHistory: BarberHistoryItem[] = [
        {
            id: 1,
            barberName: "Felipe",
            contact: "(88) 99999-1111",
            email: "barber@email.com",
            date: "12/12/2025",
            services: "Barba e cabelo",
            image: exemplo
        },
        {
            id: 2,
            barberName: "Joao",
            contact: "(88) 11111-2222",
            email: "barber@email.com",
            date: "12/12/2025",
            services: "Barba e cabelo",
            image: exemplo
        },
        {
            id: 3,
            barberName: "Alisson",
            contact: "(88) 33333-4444",
            email: "barber@email.com",
            date: "12/12/2025",
            services: "Barba e cabelo",
            image: exemplo
        }
    ]

    return(
        <>
        <div className="container">
            <header>
                <p onClick={() =>{
                window.location.href = "/home"}} 
                ><img src={voltar} alt="Botao voltar" /></p>
                <h1>
                    Histórico
                </h1>
            </header>
            <div className="content-histoy">
                <ol id="history-list">
                    {listHistory.length === 0 ? (
                        <li className="empty-message">
                            Você não tem agendamentos antigos
                        </li>
                    ) : (
                            listHistory.map((item, index)=> (
                                <li key={index}>
                                    <div className={item.barberName}>
                                        <img src={item.image} alt="Foto do barbeiro" width={150}/>
                                        <p className="name">
                                            <span>Nome:</span> {item.barberName}
                                        </p>
                                        <p className="contact">
                                            <span>Contato:</span> {item.contact}
                                        </p>
                                        <p className="email">
                                            <span>Email:</span> {item.email}
                                        </p>
                                        <p className="date">
                                            <span>Data:</span> {item.date}
                                        </p>
                                        <p className="services">
                                            <span>Serviços:</span> {item.services}
                                        </p>
                                    </div>
                                </li>
                            ))
                        )}
                </ol>
            </div>
        </div>
        </>
    )
}

export default HistoryPage