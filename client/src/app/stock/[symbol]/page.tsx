'use client'

import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

export default function Stock({ params }: { params: { symbol: string } }) {

    const isMounted = useRef(false);
    const [data, setData] = useState([]);

    useEffect(() => {
        if (isMounted.current) {
            const fetchData = async () => {
                const response = await fetch(`http://127.0.0.1:5000/stock-price-history/${params.symbol}`);
                const data = await response.json();
                setData(data.slice(-20).map(d => ({ ...d, Date: d3.timeParse("%d/%m/%Y")(d.Date) })));

            };

            fetchData();
        } else {
            isMounted.current = true;
        }
    }, [params.symbol]);

    useEffect(() => {
        if (data.length > 0) {
            const margin = { top: 20, right: 20, bottom: 30, left: 50 };
            const width = 960 - margin.left - margin.right;
            const height = 500 - margin.top - margin.bottom;

            const x = d3.scaleTime()
                .domain(d3.extent(data, d => d.Date))
                .range([0, width]);

            const y = d3.scaleLinear()
                .domain([0, d3.max(data, d => d.Close)])
                .range([height, 0]);

            const line = d3.line()
                .x(d => x(d.Date))
                .y(d => y(d.Close));

            d3.select("#chart").selectAll("*").remove();

            const svg = d3.select("#chart")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", `translate(${margin.left},${margin.top})`);

            svg.append("g")
                .attr("transform", `translate(0,${height})`)
                .call(d3.axisBottom(x));

            svg.append("g")
                .call(d3.axisLeft(y));

            svg.append("path")
                .datum(data)
                .attr("fill", "none")
                .attr("stroke", "steelblue")
                .attr("stroke-width", 1.5)
                .attr("d", line);
        }
    }, [data]);

    return (
        <div>
            <h1 className="text-3xl text-center mb-4">{params.symbol.toUpperCase()} Price prediction</h1>
            <div id="chart"></div>
        </div>
    );
}