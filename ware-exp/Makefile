all: run.ipynb

clean:
	rm run.ipynb

SNIPPETS := ../fabric-snippets/fab-config.md ../fabric-snippets/reserve-resources.md ../fabric-snippets/configure-resources.md ../fabric-snippets/offload-off.md ../fabric-snippets/draw-topo-detailed-labels.md ../fabric-snippets/log-in.md ../fabric-snippets/delete-slice.md
run.ipynb: $(SNIPPETS) custom-snippets/intro.md custom-snippets/configure-network.md
	pandoc --wrap=none \
                -i custom-snippets/intro.md \
		../fabric-snippets/fab-config.md \
                ../fabric-snippets/reserve-resources.md \
		../fabric-snippets/configure-resources.md \
		../fabric-snippets/offload-off.md  \
		../fabric-snippets/draw-topo-detailed-labels.md \
		../fabric-snippets/log-in.md \
		custom-snippets/configure-network.md \
		../fabric-snippets/delete-slice.md \
                -o run.ipynb  
