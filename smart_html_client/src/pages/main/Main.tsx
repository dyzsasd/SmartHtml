import React from "react";

import PromptInput from "../../components/PromptInput"
import styles from './Main.module.scss';


const Main: React.FC = () => {
    return <div className={styles.main}>
        <PromptInput/>
    </div>
}

export default Main;
