import { useState } from 'react';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient('https://nzajymgnizugrvymblsm.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im56YWp5bWduaXp1Z3J2eW1ibHNtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDEwOTU3MzAsImV4cCI6MjAxNjY3MTczMH0.tybCRweBV69W-ZqHGTWx3ytSKMhluhvz0rQC5Tv5NHE');

const StockSearchBar = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [suggestions, setSuggestions] = useState([]);

    const handleSearch = async (term: string) => {

        if (term === '') {
            setSuggestions([]);
            return;
        }

        const { data, error } = await supabase
            .from('nasdaq_constituent')
            .select('symbol, name')
            .ilike('name', `%${term}%`)


        if (error) {
            console.error('Error fetching symbols:', error);
        } else {
            console.log(data);
            setSuggestions(data);
        }
    };

    const handleChange = (e) => {
        setSearchTerm(e.target.value);
        handleSearch(e.target.value);
    };

    return (
        <div className="flex flex-col items-center justify-center h-full w-full">
            <input
                type="text"
                value={searchTerm}
                onChange={handleChange}
                className="text-black"
            />
            <div>
                {suggestions.map((suggestion) => (
                    <div key={suggestion.symbol} className="bg-white text-black border-b border-black">
                        <a href={`http://localhost:3000/stock/${suggestion.symbol.toLowerCase()}`} className="text-black">
                            <div className="text-center">
                                <h3 className="text-black">{suggestion.symbol}</h3>
                                <h6 className="text-black">{suggestion.name}</h6>
                            </div>
                        </a>
                    </div>
                ))}
            </div>
            <div className="flex flex-col ">


            </div>
        </div>
    );
};

export default StockSearchBar; 