import React from "react"

import styles from "./PromptInput.module.scss";


const PromptInput: React.FC = () => {
    return <div className={styles["prompt-input"]}>
        <input type="text" />
    </div>
}

export default PromptInput;
