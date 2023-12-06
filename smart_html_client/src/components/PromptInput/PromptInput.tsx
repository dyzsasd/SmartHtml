import React, { useState } from "react"

import styles from "./PromptInput.module.scss";

interface PromptInputProps{
    handleEnterDown: () => void;
}

const PromptInput: React.FC<PromptInputProps> = ({handleEnterDown}) => {

    const [prompt, setPrompt] = useState<string>();

    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setPrompt(event.target.value);
    };
    
    const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (!event.shiftKey && event.key === 'Enter') {
            event.preventDefault();
            handleEnterDown()
            console.log('Enter was pressed, your prompt is:', prompt);
        }
    };

    


    console.log(prompt)
    return <div className={styles["prompt-textarea"]}>
        
        <textarea value={prompt} rows={prompt ? prompt?.split("\n").length : 1} onChange={handleChange} onKeyDown={handleKeyDown} placeholder="Prompt"/>
    </div>
}

export default PromptInput;
