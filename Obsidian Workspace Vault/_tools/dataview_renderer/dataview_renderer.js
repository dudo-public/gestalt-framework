// _tools/export_knowledge_maps.js (全文保持ロジックで上書き)

module.exports = async (params) => {
  const { app, quickAddApi } = params;
  const dv = app.plugins.plugins["dataview"].api;
  const fs = require('fs').promises;
  const path = require('path');

  const outputDir = "_sandbox/rendered_dataviews";

  try {
    const activeFile = app.workspace.getActiveFile();
    if (!activeFile) {
      new Notice("❌ 解析対象のファイルが開かれていません。");
      return;
    }

    const content = await app.vault.read(activeFile);
    const dataviewRegex = /```dataview\s*([\s\S]*?)```/g;
    const matches = [...content.matchAll(dataviewRegex)];

    if (matches.length === 0) {
      new Notice("ℹ️ このノートに ```dataview ...``` クエリは見つかりませんでした。");
      // クエリがない場合は、元の内容をそのままコピーして終了する
      const vaultPath = app.vault.adapter.getBasePath();
      const outputVaultPath = path.join(outputDir, `${activeFile.basename}_rendered.md`);
      const absoluteOutputPath = path.join(vaultPath, outputVaultPath);
      await fs.mkdir(path.dirname(absoluteOutputPath), { recursive: true }).catch(() => {});
      await fs.writeFile(absoluteOutputPath, content, 'utf8');
      new Notice(`✅ クエリ無しのため、ファイルをそのままコピーしました: ${outputVaultPath}`);
      return;
    }

    const finalContentParts = [];
    let lastIndex = 0;
    let hasError = false;

    for (const match of matches) {
      const query = match[1];
      const originalBlock = match[0];
      const startIndex = match.index;

      // 直前のテキストを追加
      finalContentParts.push(content.substring(lastIndex, startIndex));

      try {
        const result = await dv.queryMarkdown(query, activeFile.path);
        if (result.successful) {
          // 解析結果を追加
          finalContentParts.push(result.value);
        } else {
          hasError = true;
          finalContentParts.push(`\n**Dataview Error:**\n\`\`\`\n${JSON.stringify(result, null, 2)}\n\`\`\`\n`);
        }
      } catch (e) {
        hasError = true;
        finalContentParts.push(`\n**Script Exception:**\n\`\`\`\n${e.message}\n\`\`\`\n`);
      }
      
      // カーソルを更新
      lastIndex = startIndex + originalBlock.length;
    }

    // 最後のDataviewブロック以降のテキストを追加
    finalContentParts.push(content.substring(lastIndex));

    const finalContent = finalContentParts.join('');
    const vaultPath = app.vault.adapter.getBasePath();
    const outputVaultPath = path.join(outputDir, `${activeFile.basename}_rendered.md`);
    const absoluteOutputPath = path.join(vaultPath, outputVaultPath);

    await fs.mkdir(path.dirname(absoluteOutputPath), { recursive: true }).catch(() => {});
    await fs.writeFile(absoluteOutputPath, finalContent, 'utf8');

    if (hasError) {
      new Notice(`⚠️ エラーがありましたが、 ${outputVaultPath} に結果を出力しました。`);
    } else {
      new Notice(`✅ Dataviewの結果をインラインで解析し、 ${outputVaultPath} に出力しました。`);
    }

  } catch (error) {
    new Notice("❌ スクリプト実行中に予期せぬエラーが発生しました。");
    console.error("Render Dataview Script Error:", error);
  }
};
