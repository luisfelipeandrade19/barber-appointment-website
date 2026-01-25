import { useRef } from "react";
import logo from "../../assets/logoSite.png";
import "./home.css";

function Home() {
    const servicesRef = useRef<HTMLDivElement>(null);
    const barbersRef = useRef<HTMLDivElement>(null);

    const scroll = (ref: React.RefObject<HTMLDivElement | null>, direction: "left" | "right") => {
        if (ref.current) {
            const scrollAmount = 200;
            if (direction === "left") {
                ref.current.scrollBy({ left: -scrollAmount, behavior: "smooth" });
            } else {
                ref.current.scrollBy({ left: scrollAmount, behavior: "smooth" });
            }
        }
    };

    return (
        <div className="home-container">
            <header className="home-header">
                <img src={logo} alt="Cortei Logo" className="home-logo" />
            </header>

            <section className="scroll-section">
                <div className="section-header">
                    <h2 className="section-title">Nossos Serviços:</h2>
                    <div className="scroll-controls">
                        <button className="scroll-btn" onClick={() => scroll(servicesRef, "left")}>&lt;</button>
                        <button className="scroll-btn" onClick={() => scroll(servicesRef, "right")}>&gt;</button>
                    </div>
                </div>
                <div className="horizontal-scroll-container" ref={servicesRef}>
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
                    <div className="card">
                        <div className="card-shapes">
                            <div className="shape-row">
                                <div className="shape-triangle"></div>
                            </div>
                        </div>
                    </div>
                    <div className="card">
                        <div className="card-shapes">
                            <div className="shape-triangle"></div>
                            <div className="shape-row">
                                <div className="shape-square"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section className="scroll-section">
                <div className="section-header">
                    <h2 className="section-title">Nossos Barbeiros:</h2>
                    <div className="scroll-controls">
                        <button className="scroll-btn" onClick={() => scroll(barbersRef, "left")}>&lt;</button>
                        <button className="scroll-btn" onClick={() => scroll(barbersRef, "right")}>&gt;</button>
                    </div>
                </div>
                <div className="horizontal-scroll-container" ref={barbersRef}>
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
                    <div className="card">
                        <div className="card-shapes">
                            <div className="shape-row">
                                <div className="shape-star"></div>
                                <div className="shape-square"></div>
                            </div>
                        </div>
                    </div>
                    <div className="card">
                        <div className="card-shapes">
                            <div className="shape-triangle"></div>
                        </div>
                    </div>
                </div>
            </section>


        </div>
    );
}

export default Home;