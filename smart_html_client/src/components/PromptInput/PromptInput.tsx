import React, { useState } from "react"

import styles from "./PromptInput.module.scss";
import EnterSvg from "../../assets/enter.svg?react";

interface PromptInputProps{
    handleEnterDown: (prompt: string) => void;
}

const PromptInput: React.FC<PromptInputProps> = ({handleEnterDown}) => {

    const [prompt, setPrompt] = useState<string>();

    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setPrompt(event.target.value);
    };
    
    const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (!event.shiftKey && event.key === 'Enter') {
            event.preventDefault();
            if (prompt && prompt != ""){
                handleEnterDown(prompt)
            }
        }
    };

    return <div className={styles["textarea-container"]}>
                <textarea className={styles["prompt-textarea"]} value={prompt} rows={prompt ? prompt.split("\n").length : 1} onChange={handleChange} onKeyDown={handleKeyDown} placeholder="Prompt"/>
                    <div className={prompt ? `${styles["svg-container"]} ${styles["svg-container-color"]}` : `${styles["svg-container"]}`}>
                     <EnterSvg/>
                    </div>
            </div>
}

export default PromptInput;
