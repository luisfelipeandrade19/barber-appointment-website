
import logo from "../../assets/logoSite.png";
import "./home.css";

function Home() {
    return (
        <div className="home-container">
            <header className="home-header">
                <img src={logo} alt="Cortei Logo" className="home-logo" />
            </header>

            <section>
                <h2 className="section-title">Nossos Serviços:</h2>
                <div className="horizontal-scroll-container">
                    <div className="card">
                        <div className="card-shapes">
                            <div className="shape-triangle"></div>
                            <div className="shape-row">
                                <div className="shape-star"></div>
                                <div className="shape-square"></div>
                            </div>
                        </div>
                    </div>
                    <div className="card">
                        {/* Placeholder for varied content */}
                        <div className="card-shapes">
                            <div className="shape-row">
                                <div className="shape-circle"></div>
                            </div>
                        </div>
                    </div>
                    <div className="card">
                        <div className="card-shapes"></div>
                    </div>
                </div>
            </section>

            <section>
                <h2 className="section-title">Nossos Barbeiros:</h2>
                <div className="horizontal-scroll-container">
                    <div className="card">
                        <div className="card-shapes">
                            <div className="shape-triangle"></div>
                            <div className="shape-row">
                                <div className="shape-star"></div>
                                <div className="shape-square"></div>
                            </div>
                        </div>
                    </div>
                    <div className="card">
                        <div className="card-shapes">
                            <div className="shape-row">
                                <div className="shape-triangle"></div>
                            </div>
                        </div>
                    </div>
                    <div className="card">
                        <div className="card-shapes"></div>
                    </div>
                </div>
            </section>


        </div>
    );
}

export default Home;