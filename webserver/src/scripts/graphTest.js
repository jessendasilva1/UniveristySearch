var listBlocked = [];
function renderGraph(input){
    //const links = input;
    let links = [];
    //console.log(input);
    let allNodes = [];
    input.forEach(edge => {
        let style = "solid";
        let text = ""
        if(edge.link.label){text = edge.link.label};
        if(!edge.link.required){style = "dashed"};
        links.push({
            source: edge.src.name,
            target: edge.dest.name,
            type: style,
            n1: edge.src.type_id,
            n2: edge.dest.type_id,
            label: text,
            block: edge.link.isBlocked
        });
        allNodes.push(
            {
                id: edge.src.name,
                style: edge.src.type_id,
                block: edge.src.isBlocked,
            }
        );
        allNodes.push(
            {
                id: edge.dest.name,
                style: edge.dest.type_id,
                block: edge.src.isBlocked,
            }
        );
    });
    let nodes = [...new Map(allNodes.map((item) => [item["id"], item])).values()]
    //const data = ({nodes: Array.from(new Set(links.flatMap(l => [l.source, l.target])), id => ({id})), links});
    //const nodes = data.nodes.map(d => Object.create(d));
    const data = {nodes, links};
    const types = Array.from(new Set(links.map(d => d.type)));
    //console.log(links);
    //console.log(nodes);
    const height = 1000;
    const width = 2000;
    const radius2 = 500;
    const color = d3.scaleOrdinal(types, d3.schemeCategory10);
    const color2 = d3.scaleOrdinal(d3.schemeCategory10);


    function linkArc(d) {
        //const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y);
        const r = 0;
        return `
        M${d.source.x},${d.source.y}
        A${r},${r} 0 0,1 ${d.target.x},${d.target.y}
        `;
    }

    drag = simulation => {
    
        function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
        }
        
        function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
        }
        
        function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
        }
        
        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    }

    const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id).distance(150))
        .force("charge", d3.forceManyBody().strength(-500))
        .force("x", d3.forceX())
        .force("y", d3.forceY());

    const svg = d3.select('#graphLoc').append("svg")
        .attr("id", "graphRender")
        .attr("margin", "auto")
        .attr("width", "100%")
        .attr("height", height)
        .attr("viewBox", [-width / 2, -height / 2, width, height])
        .style("font", "12px sans-serif");

    // Per-type markers, as they don't inherit styles.
    svg.append("defs").selectAll("marker")
    .data(types)
    .join("marker")
        .attr("id", d => `arrow-${d}`)
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 15)
        .attr("refY", -0.5)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
    .append("path")
        .attr("fill", color)
        .attr("d", "M0,-5L10,0L0,5");

    const link = svg.append("g")
        .attr("class", "gLink")
        .attr("fill", "none")
        .attr("stroke-width", 1.5)
    .selectAll("path")
    .data(links)
    .join("path")
        //.attr("stroke", d => color(d.type))
        .attr("stroke", function(d){
            if(d.block){
                return "#f44336";
            }
            else{
                return color(1);
            }
        })
        .attr("class", function(d) { return "link " + d.type; })
        .attr("marker-end", d => `url(${new URL(`#arrow-${d.type}`, location)})`);

    const node = svg.append("g")
        .attr("fill", "currentcolor")
        .attr("stroke-linecap", "round")
        .attr("stroke-linejoin", "round")
        .on('click', function(d) {
            console.log(d.path[1].firstChild.textContent);
            let index = listBlocked.indexOf(String(d.path[1].firstChild.textContent));
            if(index===-1) listBlocked.push(d.path[1].firstChild.textContent);
            else listBlocked.splice(index, 1);
            console.log(listBlocked);

            //Call API endpoint here once created 
		var school = document.getElementById("schoolDropdownOutput").innerText;
		var subject = document.getElementById("subjectDropdownOutput").innerText;
		subject = subject.split(/[\(\)]/)[1];
		var is_guelph;
		if (school == "University of Guelph") {
			is_guelph = true;
			is_ottawa = false;
		} else { is_guelph = false; is_ottawa = true;}
		$.ajax({
            		type: 'GET',
            		url: 'https://131.104.49.113/api/courses/graph',
            		data: {
				is_guelph: is_guelph,
				is_ottawa: is_ottawa,
				subject: subject,
				blocked: listBlocked.join(",")
			},
            		cache: true,
            		success: (result) => {
                               		let currGraph = document.getElementById("graphRender");
					if(currGraph){currGraph.remove()};
					renderGraph(result);
            		},
            		error: (err) => {
                		console.log(err);
            		}
        	});
		
          })
    .selectAll("g")
    .data(nodes)
    .join("g")
        .call(drag(simulation));

    node.append("circle")
        //.attr("fill", d => color2(d.style))
        .attr("fill", d=> {
            if(d.block){
                return "#f44336";
            }
            else{
                return color2(d.style);
            }
        })
        .attr("stroke", "white")
        .attr("stroke-width", 1.5)
        .attr("r", 7);

    const linkText = d3.selectAll(".link")
          .append("text")
          .attr("x", function(d) {
            if (d.target.x > d.source.x) {
                return (d.source.x + (d.target.x - d.source.x)/2); }
            else {
                return (d.target.x + (d.source.x - d.target.x)/2); }
            })
            .attr("y", function(d) {
                if (d.target.y > d.source.y) {
                    return (d.source.y + (d.target.y - d.source.y)/2); }
                else {
                    return (d.target.y + (d.source.y - d.target.y)/2); }
            })
            .attr("fill", "Black")
            .text(function(d){d.label});

    const linkText2 = d3.selectAll(".gLink")
            .data(links)
            .append("text")
            .attr("x", function(d) {
              if (d.target.x > d.source.x) {
                  return (d.source.x + (d.target.x - d.source.x)/2); }
              else {
                  return (d.target.x + (d.source.x - d.target.x)/2); }
              })
              .attr("y", function(d) {
                  if (d.target.y > d.source.y) {
                      return (d.source.y + (d.target.y - d.source.y)/2); }
                  else {
                      return (d.target.y + (d.source.y - d.target.y)/2); }
              })
              .attr("fill", "Black")
              .text(function(d){d.label});

    node.append("text")
        .attr("x", 8)
        .attr("y", "0.31em")
        .text(d => d.id)
    .clone(true).lower()
        .attr("fill", "none")
        .attr("stroke", "white")
        .attr("stroke-width", 3);

    simulation.on("tick", () => {
        link.attr("d", linkArc);
        node.attr("transform", d => `translate(${d.x},${d.y})`);
        //node
        //.attr("cx", function(d) { return d.x = Math.max(radius2, Math.min(width - radius2, d.x)); })
        //.attr("cy", function(d) { return d.y = Math.max(radius2, Math.min(height - radius2, d.y)); });

    });
}
    //invalidation.then(() => simulation.stop());
