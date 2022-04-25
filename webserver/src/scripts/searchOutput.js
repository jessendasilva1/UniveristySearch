class SearchOutput extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            data: props.data,
        };
        this.subjectAsc = false;
        this.courseNameAsc = false;
        this.semesterAsc = false;
        this.lecturesAsc = false;
        this.labsAsc = false;
        this.creditsAsc = false;
        this.descriptionAsc = false;
    }

	// componentDidMount(){
	// 	console.log(this.state);
	// }

  
    sortBy(key, isAsc) {
        
        let copy = this.props.data;
        let sorted = copy.sort(this.compareBy(key, isAsc));
        this.setState({data : sorted});
    }

    compareBy(key, isAsc) {
        let reverse = isAsc ? -1 : 1;
        return function(a, b) {
            let aVar = a[key];
            let bVar = b[key];
            if (key == "subject") {
                 aVar = a[key] + "*" + a["course_num"];
                 bVar = b[key] + "*" + b["course_num"];
            } else if (key == "is_offered_fall") {
                aVar = a[key] + " " + a["is_offered_winter"] + " " + a["is_offered_summer"];
                bVar = b[key] + " " + b["is_offered_winter"] + " " + b["is_offered_summer"];
            }

            if (aVar < bVar) return -1 * reverse;
            else if (aVar > bVar) return 1 * reverse;
            else return 0;
        };
    }

    render() {
      return (
        <div id="courseTableDiv">
            <table id="courseTable" className="table table-dark table-striped">
                <thead id='tableHead'>
                    <tr>
                        <th scope="col" onClick={() => {
                            this.sortBy("subject", this.subjectAsc);
                            this.subjectAsc = !this.subjectAsc;
                            }}>Course Code</th>
                        <th scope="col" onClick={() => {
                            this.sortBy("course_name", this.courseNameAsc);
                            this.courseNameAsc = !this.courseNameAsc;
                            }} >Name</th>
                        <th scope="col" onClick={() => {
                            this.sortBy("is_offered_fall",  this.semesterAsc);
                            this.semesterAsc = !this.semesterAsc;
                            }} >Semesters</th>
                        <th scope="col" onClick={() => {
                            this.sortBy("lectures", this.lecturesAsc);
                            this.lecturesAsc = !this.lecturesAsc;
                            }} >Lectures</th>
                        <th scope="col" onClick={() => {
                            this.sortBy("labs", this.labsAsc);
                            this.labsAsc = !this.labsAsc;
                        }} >Labs</th>
                        <th scope="col" onClick={() => {
                            this.sortBy("credits", this.creditsAsc);
                            this.creditsAsc = !this.creditsAsc;
                            }} >Credit Weight</th>
                        <th scope="col" onClick={() => {
                            this.sortBy("description", this.descriptionAsc);
                            this.descriptionAsc = !this.descriptionAsc;
                            }} >Description</th>
                    </tr>
                </thead>
                <tbody>
                {
                   this.props.data.map((val, key) => {
                        return (
                        <tr key={key}>
                            <td>{val.subject}*{val.course_num}</td>
                            <td>{val.course_name}</td>
                            <td>{val.is_offered_fall ? "F " : ""}{val.is_offered_winter ? "W " : ""}{val.is_offered_summer ? "S " : ""}</td>
                            <td>{val.lectures}</td>
                            <td>{val.labs}</td>
                            <td>{val.credits}</td>
                            <td id='descriptionValue'>{val.description}</td>
                        </tr>
                        );
                    }
                    
                )}
                </tbody>
            </table>
        </div>
      );
    }
  }

export default SearchOutput;