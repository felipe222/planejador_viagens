from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import TripRequest, OptimizationResult
from generator import Generator
from scraper import Scraper
from solver import Solver
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Travel Planner API")

# Permitir CORS para o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, especificar domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/optimize", response_model=OptimizationResult)
async def optimize_trip(request: TripRequest):
    try:
        logger.info(f"Received trip request: {request}")
        
        # 1. Coletar Dados (ou Mock)
        scraper = Scraper()
        
        # 2. Gerar Cenário/Entrada do Solucionador
        generator = Generator(scraper)
        solver_input = generator.generate_scenario(request)
        
        # 3. Solucionar (Otimizar)
        solver = Solver(solver_input)
        solutions = solver.solve()
        
        # 4. Retornar Resultados
        return OptimizationResult(
            solutions=solutions,
            metadata={"count": len(solutions)}
        )
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
