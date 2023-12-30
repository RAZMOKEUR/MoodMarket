'use client'
import StockSearchBar from '@/components/Stocksearchbar';


export default function Home() {

  return (
    <main>
      <h1 className="text-center text-3xl mb-10">MoodMarket </h1>
      <form >
        <StockSearchBar />

      </form>

    </main>
  )
}