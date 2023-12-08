import React, { useEffect, useState } from "react"

import styles from "./PromptInput.module.scss";
import EnterSvg from "../../assets/enter.svg?react";

interface PromptInputProps {
    handleEnterDown: (prompt: string) => void;
    loading: boolean;
}

const PromptInput: React.FC<PromptInputProps> = ({ handleEnterDown, loading}) => {

    const [prompt, setPrompt] = useState<string>();
    const [loadingViewString, setLoadingViewString] = useState<string>("");

    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setPrompt(event.target.value);
    };

    const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (!loading){
            if (!event.shiftKey && event.key === 'Enter') {
                event.preventDefault();
                if (prompt && prompt != "") {
                    handleEnterDown(prompt)
                }
            }
        }
    };

    useEffect(() => {
        if (loading) {
            const timer = setInterval(() => {
                setLoadingViewString(prev => prev.length > 3 ? "." : prev + ".");
            }, 200);
            return () => clearInterval(timer);
        }
    }, [loading]);
    
    return <div className={styles["textarea-container"]}>
        <textarea className={styles["prompt-textarea"]} value={prompt} rows={prompt ? prompt.split("\n").length : 1} onChange={handleChange} onKeyDown={handleKeyDown} placeholder="Prompt" />
        
        <div className={prompt ? `${styles["svg-container"]} ${styles["svg-container-deepen"]}` : `${styles["svg-container"]}`}>
            {loading ? <div className={styles["loading-animation-box"]}>{loadingViewString}</div> : <EnterSvg />}
        </div>
    </div>
}

export default PromptInput;
